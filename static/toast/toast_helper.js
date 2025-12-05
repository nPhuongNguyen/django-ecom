class ToastHelper{

    static variants = {
		'primary': 'primary',
		'success': 'success',
		'warning': 'warning',
		'destructive': 'destructive',
        'error': 'error',
		'info': 'info',
		'mono' : 'mono',
		'secondary' : 'secondary',
    };
    static showSuccess(
        {
            message

        }={
            message: 'Success'
        }
    ){
        KTToast.show({
            message: message,
            variant: ToastHelper.variants.success,
        });
    }
    static showError(
        {
            message
        }={
            message: 'Error'
        }
    ){
        KTToast.show({
            message: message,
            variant: ToastHelper.variants.destructive,
        });
    }

    static showWarning(
        {
            message
        }={
            message: 'Warning'
        }
    ){
        KTToast.show({
            message: message,
            variant: ToastHelper.variants.warning,
        });
    }

}