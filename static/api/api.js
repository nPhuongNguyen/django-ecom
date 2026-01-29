class CallApi {
    static async request({
        url,
        method = 'GET',
        headers = {},
        params = {},
        data = {},
        timeout = 60000 // 60 seconds
    }={}) {
        const isFormData = data instanceof FormData;
        const token = AuthStorage.getToken("Token");

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
            const res = response.data;
            return ApiResponse.format_response({
                status_code: res.status_code,
                message: res.message,
                data: res.data,
                errors: res.errors
            });
        } catch (error) {
            Logger.apiError({ url, method, error });
            return null;
        }
    }
}
