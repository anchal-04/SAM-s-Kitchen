
document.addEventListener("DOMContentLoaded", () => {
    console.log("payment.js loaded");
    const form = document.getElementById("payment");

    if (!form) {
        console.error("Form with id 'payment' not found!");
        return;
    }

    form.onsubmit = function (event) {
     clearErrors();
    // Get input values

    const expiry = document.getElementById("expiry").value;
    const state = document.getElementById("state").value;
    const zip = document.getElementById("zip").value;
    const cc = document.getElementById("cc").value;
    const phone = document.getElementById("number").value;
    const email = document.getElementById("email").value;
    const cvv = document.getElementById("cvv").value;
    const name = document.getElementById("name").value;

    // Define regex patterns
    const expiryRegex = /^\d{2}\/\d{2}$/; // MM/YY format
    const stateRegex = /^[a-zA-Z]{2}$/;  // Two letters
    const zipRegex = /^\d{5}$/;          // Five digits
    const ccRegex = /^\d{16}$/;          // Five digits
    const phRegex = /^\d{10}$/;          // Five digits
    const eRegex  = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const cvvRegex = /^\d{3}$/;          // Five digits

    let isValid = true;
    let expiryErrorMessages = "";
    // Validate expiry
    if (!expiryRegex.test(expiry)) {
        showError("expiry", "Expiry format: MM/YY format.");
        isValid = false;
    } else {
        // Additional validation for month and year
        const [month, year] = expiry.split('/');
        const monthNum = parseInt(month, 10);
        const yearNum = parseInt('20' + year, 10);
        const currentDate = new Date();
        const currentMonth = currentDate.getMonth() + 1; // getMonth() is zero-indexed
        const currentYear = currentDate.getFullYear();

        // Check if month is valid (1-12)
        if (monthNum < 1 || monthNum > 12) {
            expiryErrorMessages += "Invalid month. Must be 01-12.\n";

        }
        // Check if year is valid and not expired
        if (yearNum < currentYear ||
                 (yearNum === currentYear && monthNum < currentMonth)) {
            expiryErrorMessages +="Card is expired or invalid.\n";

        }
    }

    // If there are any error messages, show them
    if (expiryErrorMessages) {
        showError("expiry", expiryErrorMessages);
        isValid = false;
    }

    if (!name || name.trim().length === 0) {
        showError("name", "Name is a required field");
        isValid = false;
    }
    // Validate state
    if (!stateRegex.test(state)) {
        showError("state", "State must be 2 letters.");
        isValid = false;
    }

    // Validate zip
    if (!zipRegex.test(zip)) {
        showError("zip", "Zip code must be 5 digits.");
        isValid = false;
    }

       // Validate cc
    if (!ccRegex.test(cc)) {
        showError("cc", "Credit card number must be 16 digits.");
        isValid = false;
    }

       // Validate cvv
    if (!cvvRegex.test(cvv)) {
        showError("cvv", "CVV must be 3 digits.");
        isValid = false;
    }

       // Validate phone
    if (!phRegex.test(phone)) {
        showError("number", "Phone number must be 10 digits.");
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
    const inputs = document.querySelectorAll("#payment input");
    inputs.forEach(input => input.style.border = ""); // Reset borders

    // Remove all previously added error messages
    const errorMessages = document.querySelectorAll("#payment span");
    errorMessages.forEach(error => error.remove());
}
