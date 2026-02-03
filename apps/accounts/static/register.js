$(document).ready(function () {
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    const frm_register$ = $('#sign_up_form');
    const modalEl = document.querySelector('#modal-confirm');
    const modal_confirm$ = KTModal.getInstance(modalEl);
    const email$ = $('#user_email');
    const password$ = $('#user_password');
    const confirm_password$ = $('#confirm_user_password');
    function check_input(){
        let checker = true;
        if (!isValidEmail(email$.val())) {
            validator.showErrors({
                "email": "Please enter a valid email address."
            });
            checker = false;
        }
        if (password$.val() !== confirm_password$.val()) {

            validator.showErrors({
                "confirm_password": "Passwords do not match."
            });
            checker = false;
        }
        return checker;
    }

    function showConfirmModal({ title, message, email}) {
        $('#confirm_modal_title').text(title);
        $('#confirm_modal_message').text(message);
        $('#user_email_confirm').val(email);
        modal_confirm$.show();
    }
        
    const validator = FormValidateLoader.init(
        frm_register$,
        {
            submitHandler:async function (form, event) {
                if (!check_input()) return;
                MyLoading.show()
                try{
                    const formdata = FormValidateLoader.formData(frm_register$);
                    const result_api = await CallApi.request({
                        url: frm_register$.data('url'),
                        method: 'POST',
                        data: formdata
                    })
                    if (result_api){
                        if (result_api.status_code === 1){
                            showConfirmModal({
                                title: 'Mã xác nhận đã được gửi',
                                message: 'Vui lòng kiểm tra email của bạn để lấy mã xác nhận.',
                                email: formdata.email || ''
                            });
                        }else{
                            validator.showErrors(result_api.errors)
                        }
                    }
                }finally{
                    MyLoading.close()
                }
            }
        }
    )

    const confirm_form$ = $('#confirm_form');
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
                        modal_confirm$.hide();
                    }
                    else{
                        confirm_validator.showErrors(result_api.errors)
                    }
                }
            }
        }
    )
})