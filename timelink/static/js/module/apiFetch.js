async function getDataFromApi(url) {
    const resp = await fetch("/api/" + url, {
        method: "GET",
    });
    const message = await resp.json();
    return message;
}

async function putDataToApi(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    const message = await resp.json();
    return message;
}

async function postDataToApi(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    const message = await resp.json();
    message.status = resp.status;
    return message;
}

async function deleteDataFromApi(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "DELETE",
        body: JSON.stringify(data),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    const message = await resp.json();
    return message;
}

export { getDataFromApi, putDataToApi, postDataToApi, deleteDataFromApi };
