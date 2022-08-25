async function get(url) {
    const resp = await fetch("/api/" + url, {
        method: "GET",
    });
    const message = await resp.json();
    message.status = resp.status;
    return message;
}

async function put(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
    });
    const message = await resp.json();
    message.status = resp.status;
    return message;
}

async function post(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
    });
    const message = await resp.json();
    message.status = resp.status;
    return message;
}

async function remove(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "DELETE",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
    });
    const message = await resp.json();
    message.status = resp.status;
    return message;
}

export { get, put, post, remove };
