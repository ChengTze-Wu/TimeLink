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
        const groupId = document.getElementById("groupId");
        const resp = await apiFetch.post("groups", {
            data: { groupId: groupId.value },
        });
        if (resp["status"] === 200) {
            window.location.reload();
        } else if (resp["status"] === 400) {
            alert("連結失敗");
        }
        linkForm.reset();
    });
}

async function showGroup() {
    document.getElementById("groupsLoader").classList.remove("hidden");
    const resp = await apiFetch.get("groups");
    document.getElementById("groupsLoader").classList.add("hidden");
    if (resp["status"] === 200) {
        const groups = resp["data"];
        groups.forEach((group) => {
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
