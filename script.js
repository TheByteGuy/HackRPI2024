async function classifyAnimal() {
    const fileInput = document.getElementById('photo');
    const resultDiv = document.getElementById('result');
    resultDiv.innerText = ''; // Clear previous results

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