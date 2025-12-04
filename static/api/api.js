class CallApi {
    static async request(
        {
            url, 
            method = 'GET', 
            params = {}, 
            data = {}, 
            timeout = 0
        }) {
        const isFormData = data instanceof FormData;

        Logger.apiRequest({ url, method, params, data, timeout });

        try {
            const response = await axios({
                url,
                method,
                params,
                data,
                timeout: timeout > 0 ? timeout : undefined,
                headers: isFormData
                    ? { "Content-Type": "multipart/form-data" }
                    : { "Content-Type": "application/json" },
            });

            Logger.apiResponse({ url, method, response: response.data });
            return response.data;

        } catch (error) {
            Logger.apiError({ url, method, error });
            return null;
        }
    }
    
}
