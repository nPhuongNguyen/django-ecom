class SweetAlertHelper {
    static async confirmSave({
        title = 'Do you want to save changes?',
        text = '',
        icon = 'question',
        confirmButtonText = 'Yes',
        cancelButtonText = 'Cancel',
        url = null,
        method = 'POST',
        data = null,
    } = {}) {
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
            return null; 
        }
        if (url) {
            try {
                MyLoading.show();
                const minTime = 500;
                const [result_api] = await Promise.all([
                    CallApi.request(url, method, data, {}),
                    new Promise(r => setTimeout(r, minTime))
                ]);
                MyLoading.close();
                if(result_api.status == 'error'){
                    ToastHelper.error();
                    if (typeof(result_api.data) == 'object'){
                        result_api.data = CallApi.parseApiErrors(result_api.data)
                    }
                }
                else if (result_api.status == 'success'){
                    ToastHelper.success();
                }
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
        title = 'Are you sure you want to delete this item?',
        text = 'This action cannot be undone.',
        confirmButtonText = 'Delete',
        cancelButtonText = 'Cancel',
        url = null,
        method = 'DELETE',
        data = null,
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
        if (!result.isConfirmed) {
            return null; 
        }
        if (url) {
            try {
                MyLoading.show();
                const minTime = 500;
                const [result_api] = await Promise.all([
                    CallApi.request(url, method, data, {}),
                    new Promise(r => setTimeout(r, minTime))
                ]);
                MyLoading.close();
                if(result_api.status == 'error'){
                    ToastHelper.error();
                    if (typeof(result_api.data) == 'object'){
                        result_api.data = CallApi.parseApiErrors(result_api.data)
                    }
                }
                else if (result_api.status == 'success'){
                    ToastHelper.success();
                }
                return result_api;
            } catch (err) {
                console.log({
                    'err': err
                })
                ToastHelper.error();
                return null;
            }
        }
        return null
    }
}
