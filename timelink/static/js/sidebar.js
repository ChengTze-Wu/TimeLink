import * as apiFetch from "./module/apiFetch.js";

// view
function navHint() {
    const locationPath = window.location.pathname;
    let objectPath = locationPath.split("/");
    // if last path is number, remove it
    if (!isNaN(objectPath[objectPath.length - 1])) {
        objectPath.pop();
    }
    objectPath = objectPath.join("/");
    const nav_items = document.querySelectorAll(".nav_item");
    nav_items.forEach((item) => {
        const itemATag = item.querySelector("a");
        // highlight current page
        if (itemATag.pathname === objectPath) {
            item.classList.add("text-primary-green", "bg-secondary-gray");
            // can't link t the same page
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
        const response = await apiFetch.remove("auth");
        if (response.success) {
            window.location.href = "/";
        }
    });
}

async function getUserInfo() {
    const response = await apiFetch.get("user");
    if (response.success) {
        renderUsername(response.data.username);
    }
}

function clickMenuToggle() {
    const menuToggle = document.getElementById("menu_toggle");
    const menu = document.getElementById("menu");
    const menuClose = document.getElementById("menu_close");
    const nav = document.getElementById("nav");
    const userMenu = document.getElementById("user_menu");
    menuToggle.addEventListener("click", () => {
        if (menu.classList.contains("hidden")) {
            menu.classList.remove("hidden");
            menuClose.classList.add("hidden");
            nav.classList.add("hidden");
            userMenu.classList.add("hidden");
            userMenu.classList.remove("flex");
        } else {
            menu.classList.add("hidden");
            menuClose.classList.remove("hidden");
            nav.classList.remove("hidden");
            userMenu.classList.remove("hidden");
            userMenu.classList.add("flex");
        }
    });
}

function main() {
    navHint();
    logout();
    getUserInfo();
    clickMenuToggle();
}

main();
