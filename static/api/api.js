class CallApi {
    static parseApiErrors(apiErrors) {
        const errors = {};
        if (typeof apiErrors === 'object') {
            for (const field in apiErrors) {
                if (apiErrors.hasOwnProperty(field)) {
                    errors[field] = Array.isArray(apiErrors[field])
                        ? apiErrors[field].join(", ")
                        : apiErrors[field];
                }
            }
        }
        return errors;
    }

    static async request(url, method = "GET", data = null, headers = {}) {
        try {
            let body = null;
            if (data instanceof FormData) {
                body = data;
                for (let [key, value] of data.entries()) {
                    console.log(key, value);
                }
            } else if (data && typeof data === 'object') {
                body = JSON.stringify(data);
                headers["Content-Type"] = "application/json";
                console.log('body',body);
            }   
            const res = await fetch(url, { method, headers, body });
            let resData = null;

            const contentType = res.headers.get("Content-Type") || "";
            if (contentType.includes("application/json")) {
                try {
                    resData = await res.json();
                } catch (e) {
                    resData = null;
                }
            } else {
                resData = await res.text();
            }

            if (!res.ok) {
                return { status: "error", statusCode: res.status, data: resData };
            }

            return { status: "success", statusCode: res.status, data: resData };
        } catch (err) {
            return { status: "catch", error: err };
        }
    }

}
