// Handle form submission (optional feature)

document.addEventListener("DOMContentLoaded", () => {
    console.log("contact.js loaded");
    const form = document.getElementById("contact-form");

    if (!form) {
        console.error("Form with id 'contact-form' not found!");
        return;
    }

    form.onsubmit = function (event) {
     clearErrors();
    // Get input values
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const msg = document.getElementById("message").value;

    // Define regex patterns

    const eRegex  = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    let isValid = true;
    // if (!name || name.trim().length === 0) {
    //     showError("name", "Name is a required field");
    //         isValid = false;
    // }
    if (!msg || msg.trim().length === 0) {
        showError("message", "Message is a required field");
            isValid = false;
    }

           // Validate email
    if (!eRegex.test(email)) {
        showError("email", "Email format must be xxx@xxx.xxx");
        isValid = false;
    }


    // If validation fails, show alert and prevent form submission
    if (!isValid) {
        event.preventDefault();
        }
    else
    {

    }
    };
});
// Function to display inline error message
function showError(inputId, message) {
    const input = document.getElementById(inputId);

    // Highlight the input field with a red border
    input.style.border = "2px solid red";

    // Create an error message element
    const errorLabel = document.createElement("span");
    errorLabel.style.color = "#f75050";
    errorLabel.style.fontSize = "12px";
    errorLabel.style.marginTop = "5px";
    errorLabel.innerText = message;

    // Append the error message right below the input field
    input.parentNode.appendChild(errorLabel);
}

// Function to clear all error messages
function clearErrors() {
    const inputs = document.querySelectorAll("#contact-form input, #contact-form textarea");
    inputs.forEach(input => input.style.border = ""); // Reset borders

    // Remove all previously added error messages
    const errorMessages = document.querySelectorAll("#contact-form span");
    errorMessages.forEach(error => error.remove());
}