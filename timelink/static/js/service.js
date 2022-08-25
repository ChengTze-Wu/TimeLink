import * as apiFetch from "./module/apiFetch.js";
// view
function alert(message) {
    const alert = document.createElement("div");
    alert.classList.add(
        "fixed",
        "top-1",
        "right-1/2",
        "w-fit",
        "h-fit",
        "z-10",
        "translate-x-[50%]"
    );
    alert.innerHTML = `
        <div class="bg-red-500 opacity-90 p-3 rounded-xl">
            <p class="text-white text-center">${message}</p>
        </div> 
    `;
    document.body.appendChild(alert);
    setTimeout(() => {
        alert.remove();
    }, 1000);
}

function renderMessage(node, message) {
    const messageP = document.createElement("p");
    messageP.className =
        "absolute right-1/2 top-1/2 translate-y-[-50%] translate-x-[50%] w-full text-center text-gray-500";
    messageP.textContent = message;
    node.appendChild(messageP);
}

function renderGroup(name, image, id) {
    const container = document.getElementById("groups_container");
    const group = document.createElement("button");
    group.classList.add("flex-none");
    group.setAttribute("data-id", id);
    group.innerHTML = `
        <img class="w-12 h-12 mx-auto mb-1 rounded-full" src="${image}" alt="${name}">
        <p class="text-center">${name}</p>
    `;
    container.appendChild(group);
}

function renderServices(id, name, price, type, openTime, closeTime) {
    const container = document.getElementById("services_container");
    const service = document.createElement("tr");
    service.classList.add(
        "border-b",
        "border-gray-300",
        "hover:bg-gray-100",
        "text-center"
    );
    service.innerHTML = `
        <td>${name}</td>
        <td>${price}</td>
        <td>${type}</td>
        <td>${openTime}</td>
        <td>${closeTime}</td>
        <td>
            <button data-id="${id}" class="delete_btn hover:text-red-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
            </button>
        </td>`;
    container.appendChild(service);
}

function cleanServices() {
    const container = document.getElementById("services_container");
    container.innerHTML = "";
}

// controller
async function showServices(group_id) {
    cleanServices();
    // spinner start
    document.getElementById("servicesLoader").classList.remove("hidden");
    const response = await apiFetch.get(`services?group_id=${group_id}`);
    // spinner end
    document.getElementById("servicesLoader").classList.add("hidden");
    if (response.data.length > 0) {
        response.data.forEach((service) => {
            renderServices(
                service.id,
                service.name,
                service.price,
                service.type,
                service.openTime,
                service.closeTime
            );
        });
    } else {
        renderMessage(
            document.getElementById("services_container"),
            "此群組尚無服務，請新增。"
        );
    }
    deleteService(group_id);
}

async function showGroups() {
    // spinner start
    document.getElementById("servicesLoader").classList.remove("hidden");
    document.getElementById("groupsLoader").classList.remove("hidden");
    const response = await apiFetch.get("groups");
    // spinner end
    document.getElementById("servicesLoader").classList.add("hidden");
    document.getElementById("groupsLoader").classList.add("hidden");
    if (response.data.length > 0) {
        response.data.forEach((group) => {
            renderGroup(group.name, group.image, group.id);
        });
        renderMessage(
            document.getElementById("services_container"),
            "請選擇群組。"
        );
    } else {
        renderMessage(
            document.getElementById("groups_container"),
            "尚無群組，請至'Line群組管理'連結群組。"
        );
    }
}

function clickGroup() {
    const container = document.getElementById("groups_container");
    const groups = container.querySelectorAll("button");
    let lastClicked;
    groups.forEach((group) => {
        group.addEventListener("click", async () => {
            // clean last clicked hint
            if (lastClicked) {
                lastClicked.querySelector("img").classList.remove("border-2");
                lastClicked
                    .querySelector("p")
                    .classList.remove("text-primary-green");
                lastClicked.removeAttribute("disabled");
            }
            // click hint
            group.setAttribute("disabled", true);
            const image = group.querySelector("img");
            const name = group.querySelector("p");
            image.classList.add("border-2", "border-primary-green");
            name.classList.add("text-primary-green");
            // set last clicked
            lastClicked = group;

            // get services
            const id = group.getAttribute("data-id");

            await showServices(id);
        });
    });
}

function createService() {
    const serviceForm = document.getElementById("service_form");
    serviceForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(serviceForm);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        const group = document
            .getElementById("groups_container")
            .querySelector("button[disabled]");

        if (group) {
            data.group_id = group.getAttribute("data-id");
            const response = await apiFetch.post("services", data);
            if (response.status === 201) {
                serviceForm.reset();
                showServices(data.group_id);
            } else {
                alert("Something went wrong");
            }
        } else {
            alert("請先選擇群組");
            return;
        }
    });
}

function deleteService(group_id) {
    const deleteBtns = document.querySelectorAll(".delete_btn");
    deleteBtns.forEach((btn) => {
        btn.addEventListener("click", async () => {
            const service_id = btn.getAttribute("data-id");
            const response = await apiFetch.remove(`services/${service_id}`);
            if (response.status === 200) {
                showServices(group_id);
            } else {
                alert("刪除失敗");
            }
        });
    });
}

async function init() {
    flatpickr("#openTime", {
        enableTime: true,
        noCalendar: true,
        minuteIncrement: 30,
        dateFormat: "H:i",
    });
    flatpickr("#closeTime", {
        enableTime: true,
        noCalendar: true,
        minuteIncrement: 30,
        dateFormat: "H:i",
    });
}

// main exc
async function main() {
    await init();
    await showGroups();
    clickGroup();
    createService();
}

main();
