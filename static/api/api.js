class CallApi {
    static async request(url, method = "GET", body = null, headers = {}) {
        const res = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json", ...headers },
            body: body ? JSON.stringify(body) : null
        });

        if (!res.ok) {
            const msg = await res.text().catch(() => "Request failed");
            throw new Error(msg);
        }

        return await res.json().catch(() => ({}));
    }
}
