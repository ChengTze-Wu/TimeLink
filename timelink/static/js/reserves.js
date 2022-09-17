import * as apiFetch from "./module/apiFetch.js";
// var
let requestStatus = false;
const socket = io();
// model
// view
function renderMessage(node, message, className) {
    const messageP = document.createElement("p");
    messageP.textContent = message;
    messageP.className = className;
    node.appendChild(messageP);
}

function removeMessage(node) {
    const messageP = node.querySelector(".message");
    if (messageP) {
        node.removeChild(messageP);
    }
}

function renderGroups(id, groupId, img, name) {
    const container = document.getElementById("groups_container");
    const group = document.createElement("button");
    const groupImg = document.createElement("img");
    const groupName = document.createElement("p");

    group.setAttribute("group_id", id);
    group.setAttribute("groupId", groupId);
    group.className =
        "group shrink-0 hover:cursor-pointer hover:text-primary-green";
    groupImg.src = img;
    groupImg.className = "mx-auto w-12 h-12 mb-1 rounded-full";
    groupName.textContent = name;

    group.appendChild(groupImg);
    group.appendChild(groupName);
    container.appendChild(group);
}

function renderReserve(
    reserve_id,
    reserve_bookedDateTime,
    reserve_createDateTme,
    member_id,
    member_image,
    member_name,
    service_id,
    service_name,
    new_data = false
) {
    const container = document.getElementById("reserves_container");
    const reserveTr = document.createElement("tr");
    const memberTd = document.createElement("td");
    const memberImg = document.createElement("img");
    const serviceTd = document.createElement("td");
    const bookedDateTimeTd = document.createElement("td");
    const createDateTimeTd = document.createElement("td");

    reserveTr.setAttribute("reserve_id", reserve_id);
    memberTd.setAttribute("member_id", member_id);
    serviceTd.setAttribute("service_id", service_id);

    reserveTr.className = "hover:bg-gray-100 cursor-pointer";
    memberTd.className = "border border-slate-300 p-1";
    memberImg.className = "w-10 h-10 sm:inline-block rounded-full mx-1";
    serviceTd.className = "border border-slate-300 p-1";
    bookedDateTimeTd.className = "border border-slate-300 p-1";
    createDateTimeTd.className = "border border-slate-300 p-1 relative";

    memberImg.src = member_image;
    memberTd.appendChild(memberImg);
    memberTd.appendChild(document.createTextNode(member_name));
    serviceTd.textContent = service_name;
    bookedDateTimeTd.textContent = reserve_bookedDateTime;
    createDateTimeTd.appendChild(
        document.createTextNode(reserve_createDateTme)
    );

    if (new_data) {
        const newHint = document.createElement("img");
        newHint.src =
            "https://d43czlgw2x7ve.cloudfront.net/timelink/new_tag2.png";
        newHint.className =
            "w-9 h-9 inline-block mx-2 absolute right-0 top-1/2 transform -translate-y-1/2";
        createDateTimeTd.appendChild(newHint);
        reserveTr.classList.remove("cursor-pointer");
        reserveTr.classList.add("bg-gray-100");
    }

    reserveTr.appendChild(memberTd);
    reserveTr.appendChild(serviceTd);
    reserveTr.appendChild(bookedDateTimeTd);
    reserveTr.appendChild(createDateTimeTd);
    container.appendChild(reserveTr);
}
// controller
async function showGroups() {
    const response = await apiFetch.get("groups");
    document.getElementById("groupLoader").classList.add("hidden");

    if (response.success) {
        response.data.forEach((group) => {
            renderGroups(group.id, group.groupId, group.image, group.name);
        });
    } else {
        renderMessage(
            document.getElementById("groups_container"),
            "請先至'Line 群組管理'連結群組。",
            "message text-gray-500 w-full h-full flex justify-center items-center"
        );
    }
}

async function showReserves(group_id, groupId) {
    removeMessage(document.getElementById("reservesCard"));
    if (!requestStatus) {
        requestStatus = true;
        document.getElementById("reservesLoader").classList.remove("hidden");
        const response = await apiFetch.get(`reserves?group_id=${group_id}`);
        requestStatus = false;
        document.getElementById("reservesLoader").classList.add("hidden");
        if (response.success) {
            response.data.forEach((reserve) => {
                renderReserve(
                    reserve.reserve_id,
                    reserve.reserve_bookedDateTime,
                    reserve.reserve_createDateTime,
                    reserve.member_id,
                    reserve.member_image,
                    reserve.member_name,
                    reserve.service_id,
                    reserve.service_name
                );
            });
        } else {
            renderMessage(
                document.getElementById("reservesCard"),
                "尚無預約資料",
                "message text-gray-500 text-lg absolute top-1/2 right-1/2 translate-y-[-50%] translate-x-[50%]"
            );
        }
        socket.emit("join", {
            groupId: groupId,
            userId: "admin",
        });
    }
}

function clickGroup() {
    const groups = document.querySelectorAll(".group");
    const reserves = document.getElementById("reserves_container");
    let last_click = null;
    groups.forEach((group) => {
        group.addEventListener("click", async () => {
            const group_id = group.getAttribute("group_id");
            const groupId = group.getAttribute("groupId");

            if (last_click !== group && last_click !== null) {
                last_click
                    .querySelector("p")
                    .classList.remove("text-primary-green");
                last_click
                    .querySelector("img")
                    .classList.remove("border-solid");
                last_click.querySelector("img").classList.remove("border-2");
                last_click
                    .querySelector("img")
                    .classList.remove("border-primary-green");
                last_click.toggleAttribute("disabled");
                last_click.classList.add("hover:cursor-pointer");
            }
            group.querySelector("p").classList.add("text-primary-green");
            group.querySelector("img").classList.add("border-2");
            group.querySelector("img").classList.add("border-solid");
            group.querySelector("img").classList.add("border-primary-green");
            group.toggleAttribute("disabled");
            group.classList.remove("hover:cursor-pointer");
            reserves.innerHTML = "";
            if (last_click) {
                socket.emit("leave", {
                    groupId: last_click.getAttribute("groupId"),
                    userId: "admin",
                });
            }
            last_click = group;
            await showReserves(group_id, groupId);
            clickReserve();
        });
    });
}

function clickReserve() {
    const reserves = document.querySelectorAll("#reserves_container tr");
    reserves.forEach((reserve) => {
        reserve.addEventListener("click", () => {
            const reserve_id = reserve.getAttribute("reserve_id");
            window.location.href = `/board/reserve/${reserve_id}`;
        });
    });
}

function init() {
    const groups = document.querySelectorAll(".group");
    if (groups.length > 0) {
        groups[0].click();
    } else {
        document.getElementById("reservesLoader").classList.add("hidden");
    }
}

async function main() {
    await showGroups();
    clickGroup();
    init();
    socket.on("reserve_client", (socket_data) => {
        renderReserve(
            socket_data.reserve_id,
            socket_data.reserve_bookedDateTime,
            socket_data.reserve_createDateTime,
            socket_data.member_id,
            socket_data.member_image,
            socket_data.member_name,
            socket_data.service_id,
            socket_data.service_name,
            true
        );
    });
}

main();
