import * as apiFetch from "./module/apiFetch.js";

function showLogin() {
    const loginCard = document.getElementById("login_card");
    const loginBtn = document.getElementById("login_btn");
    loginBtn.addEventListener("click", async () => {
        // if already logged in, redirect to board page
        const response = await apiFetch.get("user");
        if (response.success) {
            window.location.href = "/board/guide";
        } else {
            loginCard.classList.toggle("invisible");
        }
    });
}

function close() {
    const loginCard = document.getElementById("login_card");
    const closeBtn = document.getElementById("close_btn");
    closeBtn.addEventListener("click", () => {
        loginCard.classList.add("invisible");
    });
}

function login() {
    const loginForm = document.getElementById("login-form");
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(loginForm);
        const response = await apiFetch.post("auth", formData);
        if (response.success) {
            window.location.href = "/board/guide";
        } else {
            alert("Login failed");
        }
    });
}

showLogin();
login();
close();