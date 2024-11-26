
// document.addEventListener("DOMContentLoaded", () => {
//     const form = document.querySelector(".needs-validation");
  
//     form.addEventListener("submit", (event) => {
//       let isValid = true;
  
//       // Username validation
//       const usernameField = form.querySelector("[name='username']");
//       if (!usernameField.value.trim()) {
//         isValid = false;
//         setError(usernameField, "Please, enter your username!");
//       } else {
//         clearError(usernameField);
//       }
  
//       // Email validation
//       const emailField = form.querySelector("[name='email']");
//       if (!validateEmail(emailField.value.trim())) {
//         isValid = false;
//         setError(emailField, "Please enter a valid Email address!");
//       } else {
//         clearError(emailField);
//       }
  
//       // Password validation
//       const passwordField = form.querySelector("[name='password1']");
//       if (passwordField.value.length < 6) {
//         isValid = false;
//         setError(passwordField, "Password must be at least 6 characters long!");
//       } else {
//         clearError(passwordField);
//       }
  
//       // Confirm Password validation
//       const confirmPasswordField = form.querySelector("[name='password2']");
//       if (confirmPasswordField.value !== passwordField.value) {
//         isValid = false;
//         setError(confirmPasswordField, "Passwords do not match!");
//       } else {
//         clearError(confirmPasswordField);
//       }
  
//       // Prevent submission if invalid
//       if (!isValid) {
//         event.preventDefault();
//         event.stopPropagation();
//       }
//     });
  
//     // Helper Functions
//     function setError(element, message) {
//       const feedback = element.parentElement.querySelector(".invalid-feedback");
//       element.classList.add("is-invalid");
//       feedback.textContent = message;
//     }
  
//     function clearError(element) {
//       const feedback = element.parentElement.querySelector(".invalid-feedback");
//       element.classList.remove("is-invalid");
//       feedback.textContent = "";
//     }
  
//     function validateEmail(email) {
//       const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//       return regex.test(email);
//     }
//   });
  