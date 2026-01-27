class SweetAlertHelper {

    static Icons = {
        success: 'success',
        error: 'error',
        warning: 'warning',
        info: 'info',
        question: 'question'
    };

    static async confirmSave({
        title = gettext('Do you want to save changes?'),
        text = '',
        icon = SweetAlertHelper.Icons.question,
        confirmButtonText = gettext('Yes'),
        cancelButtonText = gettext('Cancel'),
        url = null,
        method = 'POST',
        params = {},
        data = {},
        timeout = 0
    }={}) {
        const result = await Swal.fire({
            title,
            text,
            icon,
            showCancelButton: true,
            confirmButtonText,
            cancelButtonText,
            reverseButtons: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#6c757d'
        });
        if (!result.isConfirmed) {
                return Sweetalert2Response.format_response({
                confirmed: false,
                data: null
            });
        }
        if (url) {
            const result_api = await CallApi.request(
                {
                    url, 
                    method, 
                    params, 
                    data, 
                    timeout
                }
            );
            return Sweetalert2Response.format_response({
                confirmed: true,
                data: result_api
            });
        }
        return Sweetalert2Response.format_response({
            confirmed: true,
            data: null
        });
    }

    static async confirmDelete({
        title = gettext('Are you sure you want to delete this item?'),
        text = gettext('This action cannot be undone.'),
        confirmButtonText = gettext('Delete'),
        cancelButtonText = gettext('Cancel'),
        url = "",
        method = 'POST',
        params = {},
        data = {},
        timeout = 0
    }={}) {
        const result = await Swal.fire({
            title,
            text,
            icon: SweetAlertHelper.Icons.warning,
            showCancelButton: true,
            confirmButtonText,
            cancelButtonText,
            reverseButtons: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6'
        });

        if (!result.isConfirmed) {
                return Sweetalert2Response.format_response({
                confirmed: false,
                data: null
            });
        }

        if (url) {
            const result_api = await CallApi.request(
                {
                    url, 
                    method, 
                    params, 
                    data, 
                    timeout
                });
            return Sweetalert2Response.format_response({
                confirmed: true,
                data: result_api
            });
        }
        return Sweetalert2Response.format_response({
            confirmed: true,
            data: null
        });
    }

    static async NotiError({
        title = 'Thông báo',
        text = 'Đã xảy ra sự cố. Vui lòng thử lại sau.'
    } = {}) {
        await Swal.fire({
            title,
            text,
            icon: SweetAlertHelper.Icons.error,
            confirmButtonText: "OK"
        });
    }

}
