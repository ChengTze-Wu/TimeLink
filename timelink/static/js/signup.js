import * as apiFetch from "./module/apiFetch.js";

function signup() {
    const signupForm = document.getElementById("signup-form");
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(signupForm);

        const response = await apiFetch.post("user", formData);
        if (response.success) {
            window.location.href = "/";
        } else {
            alert("Signup failed");
        }
    });
}

signup();
