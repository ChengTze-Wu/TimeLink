import * as apiFetch from "./module/apiFetch.js";
// view
function renderGroups(name, createDatetime) {
    const groupList = document.getElementById("group_list");
    const trnode = document.createElement("tr");
    const nameNode = document.createElement("td");
    const createDatetimeNode = document.createElement("td");

    nameNode.textContent = name;
    createDatetimeNode.textContent = createDatetime;

    trnode.appendChild(nameNode);
    trnode.appendChild(createDatetimeNode);
    groupList.appendChild(trnode);
}

function renderInputHint(target, message) {
    const hint = document.createElement("div");
    hint.textContent = message;
    target.parentNode.appendChild(hint);
    target.style = "outline: 1px solid red;";
    setTimeout(() => {
        target.style = "";
        target.parentNode.removeChild(hint);
    }, 1000);
}

// controller
function showGroups() {
    apiFetch.getDataFromApi("groups").then((d) => {
        if (!d["error"]) {
            d["data"].forEach((r) => {
                const name = r.name;
                const createDatetime = r.createDatetime;
                renderGroups(name, createDatetime);
            });
        }
    });
}

function linkGroup() {
    const linkBtn = document.getElementById("link_btn");
    linkBtn.addEventListener("click", async () => {
        const groupId = document.getElementById("groupId");
        if (groupId.validity.valid) {
            const resp = await apiFetch.postDataToApi("groups", {
                data: { groupId: groupId.value },
            });

            console.log(resp);
        } else {
            renderInputHint(groupId, groupId.validationMessage);
        }
    });
}

showGroups();
linkGroup();
