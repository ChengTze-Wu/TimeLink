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

function showGroups() {
    getDataFromApi("groups").then((d) => {
        if (!d["error"]) {
            d["data"].forEach((r) => {
                const name = r.name;
                const createDatetime = r.createDatetime;
                renderGroups(name, createDatetime);
            });
        }
    });
}

showGroups();
