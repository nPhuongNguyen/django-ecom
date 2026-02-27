$(document).ready(function () {
    const confirm_form$ = $('#verify_otp_form');
    const validator = FormValidateLoader.init(
        confirm_form$,
        {
            submitHandler:async function (form, event) {
                event.preventDefault();
                const formdata = FormValidateLoader.formData(confirm_form$);
                const result_api = await CallApi.request({
                    url: confirm_form$.data('url'),
                    method: 'POST',
                    data: formdata
                })
                if (result_api == null || result_api.status_code == 500){
                    SweetAlertHelper.NotiError();
                    return;
                }else if (result_api.status_code !== 1){
                    ToastHelper.showError();
                    validator.showErrors(result_api.errors);
                    return;
                }else{
                    ToastHelper.showSuccess();
                    setTimeout(()=>{
                        window.location.href = confirm_form$.data('url-login');
                    },500);
                }    
            }
        }
    )
})
