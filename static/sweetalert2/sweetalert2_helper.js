class SweetAlertHelper {
    static confirmSave({
        title = gettext('Do you want to save changes?'),
        text = '',
        icon = 'question',
        confirmButtonText = gettext('Yes'),
        cancelButtonText = gettext('Cancel'),
        url = null,
        method = 'POST',
        data = null,
    } = {}) {
        const result = Swal.fire({
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
            return null; 
        }
        if (url) {
            try {
                MyLoading.show();
                const minTime = 500;
                const [result_api] = Promise.all([
                    CallApi.request(url, method, data, {}),
                    new Promise(r => setTimeout(r, minTime))
                ]);
                MyLoading.close();
                return result_api;
            } catch (err) {
                console.log({
                    'err': err
                })
                ToastHelper.error();
                return null;
            }
        }
        return null;
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
    } = {}) {
        const result = await Swal.fire({
            title,
            text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText,
            cancelButtonText,
            reverseButtons: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6'
        });

        if (!result.isConfirmed) return null; 

        if (url) {
            MyLoading.show();
            try {
                await new Promise(resolve => setTimeout(resolve, 1500));
                const res = await CallApi.request(url, method, params, data, timeout);
                if (res) {
                    ToastHelper.success();
                } else {
                    ToastHelper.error();
                } 
                return res || null;
            } finally {
                MyLoading.close();
            }
        }
        return null;
    }


}
