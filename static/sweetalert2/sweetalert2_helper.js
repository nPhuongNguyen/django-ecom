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
        return result.isConfirmed;
    }

    static async confirmDelete({
        title = gettext('Are you sure you want to delete this item?'),
        text = gettext('This action cannot be undone.'),
        confirmButtonText = gettext('Delete'),
        cancelButtonText = gettext('Cancel'),
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

        return result.isConfirmed;
    }

    static async NotiError({
        title = 'Thông báo',
        text = 'Đã xảy ra sự cố. Vui lòng thử lại sau.'
    } = {}) {
        await Swal.fire({
            title,
            text,
            icon: SweetAlertHelper.Icons.error,
            confirmButtonText: "OK",
            heightAuto: false, // Ép buộc không tự động điều chỉnh chiều cao của layout
        });
    }

}
