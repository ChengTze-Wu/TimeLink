import * as apiFetch from "./module/apiFetch.js";

// view
function navHint() {
    const locationHref = window.location.href;
    const nav_items = document.querySelectorAll(".nav_item");
    nav_items.forEach((item) => {
        const itemATag = item.querySelector("a");
        // highlight current page
        if (itemATag.href === locationHref) {
            item.classList.add("text-primary-green", "bg-secondary-gray");
            // can't link to the same page
            itemATag.removeAttribute("href");
            itemATag.classList.remove("hover:opacity-75");
        }
    });
}

function renderUsername(username) {
    const usernameNode = document.getElementById("username");
    usernameNode.textContent = username;
}

// controller
function logout() {
    const logoutBtn = document.getElementById("logout_btn");
    logoutBtn.addEventListener("click", async () => {
        const resp = await apiFetch.remove("auth");
        if (resp["status"] === 200) {
            window.location.href = "/";
        }
    });
}

async function getUserInfo() {
    const resp = await apiFetch.get("user");
    if (resp["status"] === 200) {
        renderUsername(resp["data"]["username"]);
    }
}

function main() {
    navHint();
    logout();
    getUserInfo();
}

main();
