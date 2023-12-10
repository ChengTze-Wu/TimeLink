import * as apiFetch from "./module/apiFetch.js";

// view
function renderReserve(
    service_id,
    service_image,
    service_name,
    service_price,
    reserve_bookedDateTime,
    reserve_createDateTime,
    member_name,
    member_image
) {
    const serviceImage = document.querySelector("#service_image");
    const serviceName = document.querySelector("#service_name");
    const servicePrice = document.querySelector("#service_price");
    const reserveBookedDateTime = document.querySelector(
        "#reserve_bookedDateTime"
    );
    const reserveCreateDateTime = document.querySelector(
        "#reserve_createDateTime"
    );
    const memberName = document.querySelector("#member_name");
    const memberImage = document.querySelector("#member_image");

    serviceImage.src = service_image;
    serviceName.textContent = service_name;
    serviceName.setAttribute("service_id", service_id);
    servicePrice.textContent = service_price;
    reserveBookedDateTime.textContent = reserve_bookedDateTime;
    reserveCreateDateTime.textContent = reserve_createDateTime;
    memberName.textContent = member_name;
    memberImage.src = member_image;
}

// controller
async function getReserve() {
    const reserve_id = location.pathname.split("/")[3];
    const response = await apiFetch.get(`reserves/${reserve_id}`);
    renderReserve(
        response.data.service_id,
        response.data.service_image,
        response.data.service_name,
        response.data.service_price,
        response.data.reserve_bookedDateTime,
        response.data.reserve_createDateTime,
        response.data.member_name,
        response.data.member_image
    );
}

function getAvailableTime() {
    const bookingDate = document.querySelector("#booking_date");
    const bookingTime = document.querySelector("#booking_time");
    const serviceId = document.querySelector("#service_name");
    bookingDate.addEventListener("change", async () => {
        const service_id = serviceId.getAttribute("service_id");
        const date = bookingDate.value;
        const response = await apiFetch.get(
            `reserves?booking_date=${date}&service_id=${service_id}`
        );
        bookingTime.innerHTML = "";
        response.data.available_time.forEach((time) => {
            const option = document.createElement("option");
            option.value = time;
            option.textContent = time;
            bookingTime.appendChild(option);
        });
    });
}

function updateReserve() {
    const updateForm = document.querySelector("#update_form");
    updateForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const confirmMessage = confirm("確認修改?");
        if (confirmMessage) {
            const reserve_id = location.pathname.split("/")[3];
            const formData = new FormData(updateForm);
            const response = await apiFetch.put(
                `reserves/${reserve_id}`,
                formData
            );
            if (response.success) {
                alert("修改成功");
                location.reload();
            } else {
                alert("修改失敗");
            }
        }
    });
}

function deleteReserve() {
    const deleteForm = document.querySelector("#delete_form");
    deleteForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const confirmMessage = confirm("確認刪除此預約?");
        if (confirmMessage) {
            const reserve_id = location.pathname.split("/")[3];
            const response = await apiFetch.remove(`reserves/${reserve_id}`);
            if (response.success) {
                location.href = "/board/reserve";
            } else {
                alert("刪除失敗");
            }
        }
    });
}

function main() {
    getReserve();
    getAvailableTime();
    updateReserve();
    deleteReserve();
}

main();
