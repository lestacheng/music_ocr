document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const preview = document.getElementById('preview');
    const imagePreview = document.getElementById('imagePreview');
    const controls = document.getElementById('controls');
    const playButton = document.getElementById('playButton');
    const stopButton = document.getElementById('stopButton');
    const status = document.getElementById('status');

    let currentMidiFile = null;

    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                preview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        }
    });

    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showStatus('Please select a file first', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        showStatus('Processing...', 'info');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showStatus('File processed successfully!', 'success');
                currentMidiFile = data.midi_file;
                controls.style.display = 'block';
            } else {
                showStatus(data.error || 'Error processing file', 'error');
            }
        } catch (error) {
            showStatus('Error uploading file: ' + error.message, 'error');
        }
    });

    playButton.addEventListener('click', async function() {
        if (!currentMidiFile) return;

        try {
            const response = await fetch(`/play/${currentMidiFile}`);
            const data = await response.json();

            if (response.ok) {
                showStatus('Playing music...', 'success');
            } else {
                showStatus(data.error || 'Error playing music', 'error');
            }
        } catch (error) {
            showStatus('Error playing music: ' + error.message, 'error');
        }
    });

    stopButton.addEventListener('click', async function() {
        try {
            const response = await fetch('/stop');
            const data = await response.json();

            if (response.ok) {
                showStatus('Music stopped', 'success');
            } else {
                showStatus(data.error || 'Error stopping music', 'error');
            }
        } catch (error) {
            showStatus('Error stopping music: ' + error.message, 'error');
        }
    });

    function showStatus(message, type) {
        status.textContent = message;
        status.className = '';
        status.classList.add(`status-${type}`);
    }
});
