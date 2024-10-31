// main.js

// Wait for the document to fully load
document.addEventListener('DOMContentLoaded', function() {
    // Hide loader initially
    hideLoader();

    // Add event listener for the form submission
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            showLoader();  // Show loader on form submission
        });
    }
});
