import * as apiFetch from "./module/apiFetch.js";

function logout() {
    const logoutBtn = document.querySelector(".signout_icon");

    logoutBtn.addEventListener("click", async () => {
        const response = await apiFetch.deleteDataFromApi("auth");
        if (response.status === 200) {
            window.location.href = "/";
        }
    });
}

logout();
