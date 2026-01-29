$(document).ready(function () {
    const frm_login$ = $('#sign_in_form');
    const validator = FormValidateLoader.init(
        frm_login$,
        {
            submitHandler:async function (form, event) {
                MyLoading.show()
                try{
                    const formdata = FormValidateLoader.formData(frm_login$);
                    const result_api = await CallApi.request({
                        url: frm_login$.data('url'),
                        method: 'POST',
                        data: formdata
                    })
                    if (result_api){
                        if (result_api.status_code !== 1){
                            ToastHelper.showError();
                            return;
                        }
                        const check_token = AuthStorage.hasToken("Token")
                        try{
                            if (check_token == true){
                                AuthStorage.removeToken("Token")
                            }
                        }
                        finally{
                            AuthStorage.setToken("Token", result_api.data)
                        }
                        ToastHelper.showSuccess();
                    }else{
                        SweetAlertHelper.NotiError()
                    }
                }finally{
                    MyLoading.close()
                }
            }
        }
    )
    const password$ = $('#user_password');
    const eye$ = $('#eye');
    password$.on('input', function(){
        if (this.value.length > 0) {
            eye$.removeClass('hidden');
        } else {
            eye$.addClass('hidden');
        }
    })
})