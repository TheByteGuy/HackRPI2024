window.onload = function() {
    // if (localStorage.getItem("isLoggedIn") === null) {
    // localStorage.setItem("isLoggedIn", "false");
    // }
    localStorage.setItem("isLoggedIn", "false");
};

function checkLoginStatus(event) {
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  
    if (!isLoggedIn) {
      event.preventDefault();
      alert("Please register or log in first to upload a photo.");
      document.getElementById("auth-section").scrollIntoView({ behavior: "smooth" });
    }
  }

async function classifyAnimal() {
    const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

    if (!isLoggedIn) {
        alert("Please register or log in first to classify the animal.");
        return;
    }

    const fileInput = document.getElementById('photo');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    const classificationContainer = document.getElementById('classification-container');
    
    resultDiv.innerText = '';
    errorDiv.innerText = '';
    
    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';

    classificationContainer.style.display = 'none';

    if (fileInput.files.length === 0) {
        alert('Please select a photo.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('photo', file);

    CustomMarker(file)

    try {
        const response = await fetch('http://127.0.0.1:5000/classify', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to classify the animal. Please try again.');
        }

        const result = await response.json();
        
        resultDiv.innerHTML = `<h2><strong>Classification Result:</strong></h2> ${result}`;
        resultDiv.style.display = 'block'; 
        classificationContainer.style.display = 'block';

        if (users[currentUser]) {
            users[currentUser].uploads += 1; 
            localStorage.setItem('users', JSON.stringify(users));  
        }
        // Update the display of score and leaderboard
        updateScoreDisplay();
        displayLeaderboard();
    } 
    catch (error) {
        console.error('Error:', error);
        
        errorDiv.innerText = `Error: ${error.message}`;
        errorDiv.style.display = 'block'; 

        classificationContainer.style.display = 'block';
    }
}

function CustomMarker(file){
    const reader = new FileReader();
        reader.onload = function (e) {
        const iconUrl = e.target.result;  

        customIcon = {
            url: iconUrl,           
            size: new google.maps.Size(50, 60), 
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(25, 60), 
            scaledSize: new google.maps.Size(50, 60),
        };

        
        if (marker) {
            marker.setIcon(customIcon); 
        } else {
            marker = new google.maps.Marker({
            map: map,
            position: map.getCenter(),  
            icon: customIcon,          
            });
        }
        };
        reader.readAsDataURL(file);
}


function handleImageSelection(event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function(e) {
            const imagePreview = document.getElementById('preview-image');
            imagePreview.src = e.target.result;
        };

        reader.readAsDataURL(file);
    } else {
        // Handle the case where no file is selected
        const imagePreview = document.getElementById('preview-image');
        imagePreview.src = ""; // Clear the preview image
    }
}

const photoInput = document.getElementById('photo');
photoInput.addEventListener('change', handleImageSelection);


document.getElementById('photo').addEventListener('change', previewImage);

function previewImage(event) {
    const file = event.target.files[0];
    const previewImage = document.getElementById('preview-image');
    const errorDiv = document.getElementById('error');

    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            errorDiv.innerText = '';
        };
        reader.readAsDataURL(file);
    } else {
        previewImage.src = '';
        previewImage.style.display = 'none';
        errorDiv.innerText = 'Please select a valid image file.';
    }
}


// Initialize or retrieve users data from localStorage
let users = JSON.parse(localStorage.getItem('users')) || {};
let currentUser = null;

document.getElementById('photo').addEventListener('change', previewImage);

function registerOrLogin() {
    localStorage.setItem("isLoggedIn", "true");
    alert("You are now logged in!");
    const username = document.getElementById('username').value.trim();
    const errorDiv = document.getElementById('error');

    if (!username) {
        errorDiv.innerText = 'Please enter a valid username.';
        return;
    }

    // Check if user exists, if not, create a new entry
    if (!users[username]) {
        users[username] = { uploads: 0 };
    }

    // Save to localStorage
    localStorage.setItem('users', JSON.stringify(users));

    // Set the current user and update UI
    currentUser = username;
    // document.getElementById('auth-section').style.display = 'none';
    document.getElementById('uploadForm').style.display = 'block';
    document.getElementById('error').innerText = '';
    updateScoreDisplay();
    displayLeaderboard();
}

let map, marker;
// Funtion to update the marker on the map
function updateLocation() {
    const location = document.getElementById("location").value;
    if (!location) {
      alert("Please enter a location.");
      return;
    }
    geocodeLocation(location);
}

// Function to geocode the location and place a marker
function geocodeLocation(location) {
    const geocoder = new google.maps.Geocoder();
    
    geocoder.geocode({ address: location }, (results, status) => {
      if (status === "OK") {
        const position = results[0].geometry.location;
        map.setCenter(position);
        map.setZoom(12);
  
        if (marker) {
          marker.setPosition(position);
        } else {
          marker = new google.maps.Marker({
            map: map,
            position: position,
          });
        }
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
}

function updateScoreDisplay() {
    if (currentUser) {
        document.getElementById('uploadCount').innerText = users[currentUser].uploads;
    }
}

// Function to display leaderboard sorted by uploads
function displayLeaderboard() {
    const leaderboardDiv = document.getElementById('leaderboard');
    leaderboardDiv.innerHTML = '';

    const sortedUsers = Object.keys(users)
        .sort((a, b) => users[a].uploads - users[b].uploads)
        .slice(0, 10); // Display top 10 users

    sortedUsers.forEach((username, index) => {
        const userScore = users[username].uploads;
        const entry = document.createElement('div');
        entry.className = 'leaderboard-entry';
        entry.innerText = `${index + 1}. ${username} - ${userScore} uploads`;
        leaderboardDiv.appendChild(entry);
    });
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 37.7749, lng: -122.4194 },
    zoom: 8,
  });
}

// Load leaderboard on page load
displayLeaderboard();
