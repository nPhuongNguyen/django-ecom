class ToastHelper {
    static config() {
        toastr.options = {
            closeButton: false,          
            newestOnTop: true,
            progressBar: false,          
            positionClass: "toast-top-right",
            preventDuplicates: true,
            showDuration: "200",
            hideDuration: "500",
            timeOut: "3000",
            extendedTimeOut: "1000",
            showEasing: "swing",
            hideEasing: "swing",
            showMethod: "fadeIn",
            hideMethod: "fadeOut",
            tapToDismiss: true,          
            // toastClass: "toast toast-white" này để chỉnh css các thông báo
        };
    }

    static success(msg = 'Successfully!') { 
        this.config(); 
        toastr.success(msg); 
    }
    static error(msg = 'Something went wrong!') { 
        this.config(); 
        toastr.error(msg); 
    }
    static info(msg = 'Info') {
        this.config(); 
        toastr.info(msg); 
    }
    static warning(msg = 'Warning') {
        this.config();
        toastr.warning(msg); 
    }
}
