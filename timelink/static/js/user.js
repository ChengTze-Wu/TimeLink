import * as apiFetch from "./module/apiFetch.js";

function login() {
    const loginBtn = document.querySelector(".login_btn");

    loginBtn.addEventListener("click", async () => {
        // const username = document.getElementById("username").value;
        // const password = document.getElementById("password").value;
        const data = {
            username: "test",
            password: "test",
        };
        const message = await apiFetch.postDataToApi("auth", data);
        if (message.status === 200) {
            window.location.href = "/board";
        }
    });
}
login();
