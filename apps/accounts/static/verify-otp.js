$(document).ready(function () {
    const confirm_form$ = $('#verify_otp_form');
    const confirm_validator = FormValidateLoader.init(
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
                if (result_api){
                    if (result_api.status_code === 1){
                        ToastHelper.showSuccess();
                        setTimeout(()=>{
                            window.location.href = confirm_form$.data('url-login');
                        },500);
                    }
                    else{
                        confirm_validator.showErrors(result_api.errors)
                    }
                }
            }
        }
    )
})
