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

function renderGroup(groupName, groupImg, memberCount, createDate) {
    const groupContainer = document.getElementById("groups");
    const groupCard = document.createElement("div");
    groupCard.className = "card h-60";
    groupCard.innerHTML = `
        <h3 class="text-xl">${groupName}</h3>
        <img
            class="m-auto rounded-full my-2"
            width="100px"
            height="100px"
            src="${groupImg}"
        />
        <div class="flex justify-between">
            <p class="text-base">成員人數：</p>
            <p class="text-lg text-center">${memberCount}</p>
        </div>
        <div class="flex justify-between">
            <p class="text-base">連結日期：</p>
            <p class="text-base">${createDate}</p>
        </div>`;
    groupContainer.appendChild(groupCard);
}
// controller
function linkGroup() {
    const linkForm = document.getElementById("link_form");
    linkForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(linkForm);
        const response = await apiFetch.post("groups", formData);
        if (response.success) {
            window.location.reload();
        } else {
            alert("連結失敗");
        }
        linkForm.reset();
    });
}

async function showGroup() {
    document.getElementById("groupsLoader").classList.remove("hidden");
    const response = await apiFetch.get("groups");
    document.getElementById("groupsLoader").classList.add("hidden");
    if (response.success) {
        response.data.forEach((group) => {
            renderGroup(
                group.name,
                group.image,
                group.memberCount,
                group.createDate
            );
        });
    }
}

function main() {
    linkGroup();
    showGroup();
}

main();
