import * as apiFetch from "./module/apiFetch.js";

function signup() {
    const signupForm = document.getElementById("signup-form");
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(signupForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        const response = await apiFetch.post("user", data);
        if (response.status === 200) {
            window.location.href = "/";
        } else {
            alert("Signup failed");
        }
    });
}

signup();
