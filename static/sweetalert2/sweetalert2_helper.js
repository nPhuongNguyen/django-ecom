class SweetAlertHelper {

    static parseError(err) {
        try {
            return Object.values(JSON.parse(err.message)).flat().join(', ');
        } catch {
            return err.message;
        }
    }

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

        if (result.isConfirmed && url) {
            try {
                await CallApi.request(url, method, data);
                ToastHelper.success();
            } catch (err) {
                Swal.fire({
                    title: 'Error!',
                    text: SweetAlertHelper.parseError(err),
                    icon: 'error'
                });
            }
        }
    }

    static async confirmDelete({
        title = 'Are you sure you want to delete this item?',
        text = 'This action cannot be undone.',
        confirmButtonText = 'Delete',
        cancelButtonText = 'Cancel',
        url = null,
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

        if (result.isConfirmed && url) {
            try {
                await CallApi.request(url, 'DELETE');
                ToastHelper.success();
            } catch (err) {
                Swal.fire({
                    title: 'Error!',
                    text: SweetAlertHelper.parseError(err),
                    icon: 'error'
                });
            }
        }
    }
}
