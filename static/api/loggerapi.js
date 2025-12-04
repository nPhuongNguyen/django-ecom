class Logger {
    static apiRequest({ url, method, params, data, timeout }) {
        console.group(`API Request: ${method} ${url}`);
        console.log("Params:", params);

        if (data instanceof FormData) {
            console.log("Data (FormData):");
            for (let pair of data.entries()) {
                console.log(`  ${pair[0]}:`, pair[1]);
            }
        } else {
            console.log("Data:", data);
        }

        console.log("Timeout:", timeout);
        console.groupEnd();
    }


    static apiResponse({ url, method, response }) {
        console.group(`API Response: ${method} ${url}`);
        console.log("Response:", response);
        console.groupEnd();
    }

    static apiError({ url, method, error }) {
        console.group(`API Error: ${method} ${url}`);
        console.error(error);
        console.groupEnd();
    }
}
