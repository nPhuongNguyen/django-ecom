class SweetAlertHelper {
    static async confirmSave({
        title = gettext('Do you want to save changes?'),
        text = '',
        icon = 'question',
        confirmButtonText = gettext('Yes'),
        cancelButtonText = gettext('Cancel'),
        url = null,
        method = 'POST',
        params = {},
        data = {},
        timeout = 0
    }) {
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
        if (!result.isConfirmed) return null; 
        if (url) {
            try {
                MyLoading.show();
                await new Promise(resolve => setTimeout(resolve, 1500));
                console.log('Sending data to URL:', url, 'with data:', data);
                const res = await CallApi.request(
                    {
                        url, 
                        method, 
                        params, 
                        data, 
                        timeout
                    });
                return res;
            } finally {
                MyLoading.close();
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
    }) {
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
                const res = await CallApi.request(
                    {
                        url, 
                        method, 
                        params, 
                        data, 
                        timeout
                    });
                return res;
            } finally {
                MyLoading.close();
            }
        }
        return null;
    }


}
