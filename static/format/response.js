class ApiResponse {
    static format_response({
        status_code,
        message,
        data = null,
        errors = null
    }={}) {
        return {
            status_code,
            message,
            data,
            errors
        };
    }

}
