// view
function renderServices(name, price, group_name) {
    const servicesList = document.getElementById("services_list");

    const trnode = document.createElement("tr");
    const snameNode = document.createElement("td");
    const spricNode = document.createElement("td");
    const groupNameNode = document.createElement("td");

    snameNode.textContent = name;
    spricNode.textContent = price;
    groupNameNode.textContent = group_name;

    trnode.appendChild(snameNode);
    trnode.appendChild(spricNode);
    trnode.appendChild(groupNameNode);
    servicesList.appendChild(trnode);
}

function renderSelect(id, name) {
    const selectGroup = document.getElementById("select_group");
    const groupOption = document.createElement("option");
    groupOption.setAttribute("value", id);
    groupOption.textContent = name;
    selectGroup.appendChild(groupOption);
}

function showSerivces() {
    getDataFromApi("groups_option").then((d) => {
        if (!d["error"]) {
            d["data"].forEach((r) => {
                const id = r.id;
                const name = r.name;
                renderSelect(id, name);
            });
        }
    });
    getDataFromApi("services").then((d) => {
        if (!d["error"]) {
            d["data"].forEach((r) => {
                const name = r.name;
                const price = r.price;
                const group_name = r.group_name;
                renderServices(name, price, group_name);
            });
        }
    });
}

showSerivces();
