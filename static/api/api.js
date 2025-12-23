class CallApi {
    static async request({
        url,
        method = 'GET',
        headers = {},
        params = {},
        data = {},
        timeout = 0
    }={}) {
        const isFormData = data instanceof FormData;
        const token = AuthStorage.getToken();

        try {
            const response = await axios({
                url,
                method,
                params,
                data,
                timeout: timeout > 0 ? timeout : undefined,
                headers: {
                    ...headers,
                    ...( !isFormData && { 'Content-Type': 'application/json' }),
                    ...( token && { 'Token': token }),
                }
            });

            return ApiResponse.format_response(response.data);
        } catch (error) {
            Logger.apiError({ url, method, error });
            return null;
        }
    }
}
