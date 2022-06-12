// model
async function getDataFromApi(url) {
    const resp = await fetch("api/" + url, {
        method: "GET",
    });
    const message = await resp.json();
    return message;
}

async function postDataToApi(url, data) {
    const resp = await fetch("api/" + url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    const message = await resp.json();
    return message;
}

async function deleteDataToApi(url, data) {
    const resp = await fetch("api/" + url, {
        method: "DELETE",
        body: data,
    });
    const message = await resp.json();
    return message;
}
