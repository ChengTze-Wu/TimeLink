import * as apiFetch from "./module/apiFetch.js";
// view
function renderReserves(uid, uname, rname, rdate, rtime) {
    const reservesList = document.getElementById("reserves_list");
    const uidNode = document.createElement("td");
    const unameNode = document.createElement("td");
    const rnameNode = document.createElement("td");
    const rdateNode = document.createElement("td");
    const rtimeNode = document.createElement("td");

    uidNode.textContent = uid;
    unameNode.textContent = uname;
    rnameNode.textContent = rname;
    rdateNode.textContent = rdate;
    rtimeNode.textContent = rtime;

    reservesList.appendChild(uidNode);
    reservesList.appendChild(unameNode);
    reservesList.appendChild(rnameNode);
    reservesList.appendChild(rdateNode);
    reservesList.appendChild(rtimeNode);
}

function showReserves() {
    apiFetch.getDataFromApi("reserves").then((d) => {
        if (!d["error"]) {
            d["results"].forEach((r) => {
                const uid = r.uid;
                const uname = r.uname;
                const rname = r.rname;
                const rdate = r.rdate;
                const rtime = r.rtime;

                renderReserves(uid, uname, rname, rdate, rtime);
            });
        }
    });
}

// showReserves();
