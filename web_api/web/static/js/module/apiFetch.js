async function get(url) {
    const resp = await fetch("/api/" + url, {
        method: "GET",
    });
    const jsonResp = await resp.json();
    return jsonResp;
}

async function put(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "PUT",
        body: data,
        headers: {
            "X-CSRFToken": csrf_token,
        },
    });
    const jsonResp = await resp.json();
    return jsonResp;
}

async function post(url, data = null) {
    const resp = await fetch("/api/" + url, {
        method: "POST",
        body: data,
        headers: {
            "X-CSRFToken": csrf_token,
        },
    });
    const jsonResp = await resp.json();
    return jsonResp;
}

async function remove(url) {
    const resp = await fetch("/api/" + url, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": csrf_token,
        },
    });
    const jsonResp = await resp.json();
    return jsonResp;
}

export { get, put, post, remove };
