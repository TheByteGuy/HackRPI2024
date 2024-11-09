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
