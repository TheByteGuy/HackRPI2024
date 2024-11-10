async function classifyAnimal() {
    const fileInput = document.getElementById('photo');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    resultDiv.innerText = ''; // Clear previous result
    errorDiv.innerText = '';  // Clear previous error

    if (fileInput.files.length === 0) {
        alert('Please select a photo.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('photo', file);

    try {
        const response = await fetch('https://your-backend-url.com/classify', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to classify the animal. Please try again.');
        }

        const result = await response.json();
        resultDiv.innerText = `Classification Result: ${result.classification}`;
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerText = 'There was an error classifying the animal.';
    
    // MOVE BELLOW ME TO CLASSIFICATION RESULT WHEN FIXED
    // Simulate classification and increment score
    users[currentUser].uploads += 1;
    localStorage.setItem('users', JSON.stringify(users));

    // Update display
    updateScoreDisplay();
    displayLeaderboard();
    // MOVE ABOVE ME TO CLASSIFICATION RESULT WHEN FIXED
    
    }
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
            previewImage.style.display = 'block'; // Make the image visible
            errorDiv.innerText = ''; // Clear any error messages
        };
        reader.readAsDataURL(file); // Read the image file as a data URL
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
    document.getElementById('auth-section').style.display = 'none';
    document.getElementById('uploadForm').style.display = 'block';
    document.getElementById('error').innerText = '';
    updateScoreDisplay();
    displayLeaderboard();
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
        .sort((a, b) => users[b].uploads - users[a].uploads)
        .slice(0, 10); // Display top 10 users

    sortedUsers.forEach((username, index) => {
        const userScore = users[username].uploads;
        const entry = document.createElement('div');
        entry.className = 'leaderboard-entry';
        entry.innerText = `${index + 1}. ${username} - ${userScore} uploads`;
        leaderboardDiv.appendChild(entry);
    });
}


// Load leaderboard on page load
displayLeaderboard();