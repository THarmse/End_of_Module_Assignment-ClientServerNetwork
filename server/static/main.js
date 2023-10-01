// Function to escape special HTML characters
function escapeHtml(unsafe) {
    return unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

// Fetch messages from the server and update the page
function updateMessages() {
    fetch('/get_messages')
    .then(response => response.json())
    .then(data => {
        let messageDiv = document.getElementById("messages");
        messageDiv.innerHTML = '';

        document.getElementById("configSlider").checked = (data.file_or_print === 'file');

        if (data.file_or_print === 'file') {
            document.getElementById("downloadButton").style.display = 'block';
            document.getElementById("downloadClientFileButton").style.display = 'block';
            document.getElementById("filePath").style.display = 'block';
            document.getElementById("filePathText").innerText = data.file_path;
        } else {
            document.getElementById("downloadButton").style.display = 'none';
            document.getElementById("downloadClientFileButton").style.display = 'block';
            document.getElementById("filePath").style.display = 'none';
        }

        data.received_messages.forEach(message => {
            let escapedMessage = escapeHtml(message);
            messageDiv.innerHTML += `<div class="message-container">${escapedMessage}</div>`;
        });
    });
}

document.getElementById("clearButton").addEventListener("click", function() {
    fetch('/clear_messages', {
        method: 'POST',
    }).then(() => {
        updateMessages();
    });
    // Display the success message
    displaySuccessMessage('Messages Cleared Successfully!');
});

document.getElementById("downloadButton").addEventListener("click", function() {
    window.location.href = '/download_file';
    // Display the success message
    displaySuccessMessage('Download Successful!');
});

document.getElementById("downloadClientFileButton").addEventListener("click", function() {
    window.location.href = '/download_client_file';
    // Display the success message
    displaySuccessMessage('Download Successful!');
});

// Function to update server config for file or print
function updateConfig(new_value) {
    fetch('/update_config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'file_or_print': new_value })
    }).then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert("Configuration updated successfully");
        } else {
            alert("Failed to update configuration: " + data.error);
        }
    });
}

// Function to display a success message
function displaySuccessMessage(message) {
    const successMessageElement = document.getElementById('successMessage');
    successMessageElement.textContent = message;
    successMessageElement.style.display = 'block';

    // Hide the message after 3 seconds
    setTimeout(function() {
        successMessageElement.style.display = 'none';
    }, 3000);
}

// Add event listener to UI control
document.getElementById("configSlider").addEventListener("change", function() {
    let new_value = this.checked ? "file" : "print";
    updateConfig(new_value);
});

setInterval(updateMessages, 2000);
