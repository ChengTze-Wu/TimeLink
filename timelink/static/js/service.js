// view
function renderServices(id, name, type, price, group_name) {
    const servicesList = document.getElementById("services_list");
    const trnode = document.createElement("tr");
    const nameNode = document.createElement("td");
    const typeNode = document.createElement("td");
    const priceNode = document.createElement("td");
    const groupNameNode = document.createElement("td");
    const editNode = document.createElement("td");
    const trash = document.createElement("i");

    nameNode.textContent = name;
    typeNode.textContent = type;
    priceNode.textContent = price;
    groupNameNode.textContent = group_name;

    editNode.style = "width:100px;";

    editNode.classList = "text-center";
    trash.classList = "trash fa-solid fa-trash";
    trash.setAttribute("service-id", id);

    trnode.appendChild(nameNode);
    trnode.appendChild(priceNode);
    trnode.appendChild(typeNode);
    trnode.appendChild(groupNameNode);

    editNode.appendChild(trash);
    trnode.appendChild(editNode);

    servicesList.appendChild(trnode);
}

function renderOption(id, name) {
    const selectGroup = document.getElementById("select_group");
    const groupOption = document.createElement("option");
    groupOption.setAttribute("value", id);
    groupOption.textContent = name;
    selectGroup.appendChild(groupOption);
}

function startSpinner() {
    const spinners = document.querySelectorAll(".spinner");
    spinners.forEach((spinner) => {
        spinner.classList.remove("d-none");
    });
}
function stopSpinner() {
    const spinners = document.querySelectorAll(".spinner");
    spinners.forEach((spinner) => {
        spinner.classList.add("d-none");
    });
}
// controller
function cleanServices() {
    const servicesList = document.getElementById("services_list");
    while (servicesList.lastElementChild) {
        servicesList.removeChild(servicesList.lastElementChild);
    }
}

function addService() {
    const submit = document.getElementById("add_service");
    submit.addEventListener("click", async () => {
        const name = document.getElementById("name");
        const price = document.getElementById("price");
        const type = document.getElementById("type");
        const groupId = document.getElementById("select_group");
        if (name.value == "" || price.value == "" || groupId.value == "") {
        } else {
            startSpinner();
            const resp = await postDataToApi("service", {
                name: name.value,
                price: price.value,
                type: type.value,
                groupId: groupId.value,
            });
            if (resp["ok"]) {
                name.value = "";
                price.value = "";
                groupId.value = "";
                type.value = "";
            }
            await showServices();
            stopSpinner();
        }
    });
}

function deleteService() {
    const trashBtns = document.querySelectorAll(".trash");
    trashBtns.forEach((btn) => {
        btn.addEventListener("click", async () => {
            startSpinner();
            const id = btn.getAttribute("service-id");
            const resp = await deleteDataToApi("service", id);
            if (!resp["error"]) {
                await showServices();
            }
            stopSpinner();
        });
    });
}

async function showServices() {
    cleanServices();
    const resp = await getDataFromApi("services");
    if (!resp["error"]) {
        resp["data"].forEach((d) => {
            const id = d.id;
            const name = d.name;
            const type = d.type;
            const price = d.price;
            const group_name = d.group_name;
            renderServices(id, name, type, price, group_name);
        });
    }
    deleteService();
}

async function showGroupsOption() {
    const resp = await getDataFromApi("groups_option");
    if (!resp["error"]) {
        resp["data"].forEach((d) => {
            const id = d.id;
            const name = d.name;
            renderOption(id, name);
        });
    }
}

async function init() {
    showGroupsOption();
    startSpinner();
    await showServices();
    stopSpinner();
}

// main exc
async function main() {
    await init();
    addService();
}

main();
