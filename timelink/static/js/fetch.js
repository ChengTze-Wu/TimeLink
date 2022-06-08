// model
async function getDataFromApi(url) {
    const resp = await fetch("api/" + url, {
        method: "GET",
    });
    const message = await resp.json();
    return message;
}

async function postDataToApi(url, data) {
    console.log(JSON.stringify(data));
    const resp = await fetch("api/" + url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: new Headers({ "Content-Type": "application/json" }),
    });
    const message = await resp.json();
    console.log(message);
    return message;
}
