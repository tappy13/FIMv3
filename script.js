document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('file-upload-form');
    const fileInput = document.getElementById('file-input');
    const messages = document.getElementById('messages');
    const resultSection = document.getElementById('result-section');
    const resultFilename = document.getElementById('result-filename');
    const resultHash = document.getElementById('result-hash');
    const resultMetadata = document.getElementById('result-metadata');
    const resultStatus = document.getElementById('result-status');
    const backButton = document.getElementById('back-button');
    const uploadForm = document.getElementById('upload-form');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Clear previous messages
        messages.innerHTML = '';

        // Get the file from the input
        const file = fileInput.files[0];
        if (!file) {
            messages.textContent = 'Please select a file.';
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                // Display results
                resultFilename.textContent = result.filename;
                resultHash.textContent = result.hash_value;
                resultMetadata.innerHTML = '';
                for (const [key, value] of Object.entries(result.metadata)) {
                    const li = document.createElement('li');
                    li.textContent = `${key}: ${value}`;
                    resultMetadata.appendChild(li);
                }
                resultStatus.textContent = result.firebase_status;

                // Show result section
                uploadForm.style.display = 'none';
                resultSection.style.display = 'block';
            } else {
                messages.textContent = 'An error occurred while processing the file.';
            }
        } catch (error) {
            console.error('Error:', error);
            messages.textContent = 'An error occurred. Please try again.';
        }
    });

    backButton.addEventListener('click', () => {
        // Reset to the upload form
        resultSection.style.display = 'none';
        uploadForm.style.display = 'block';
        fileInput.value = '';
    });
});
