class CallApi {
    static async request(url, method = "GET", body = null, options = {}) {
        const headers = options.headers || {};
        let payload = null;

        if (body instanceof FormData) {
            payload = body; 
        } else if (body) {
            payload = JSON.stringify(body);
            headers["Content-Type"] = "application/json";
        }

        try {
            const res = await fetch(url, { method, headers, body: payload });
            const contentType = res.headers.get("Content-Type") || "";

            let data;
            if (contentType.includes("application/json")) {
                data = await res.json();
            } else {
                data = await res.text();
            }

            if (!res.ok) {
                return { status: "error", statusCode: res.status, data };
            }

            return { status: "success", data };

        } catch (err) {
            return { status: "catch", error: err };
        }
    }
}
