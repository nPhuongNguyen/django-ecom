$(document).ready(function () {
    const frm$ = $('#frm_create_attribute')
    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();
                const formdata = FormValidateLoader.formData(frm$);
                const result = await SweetAlertHelper.confirmSave({ 
                    url: frm$.data('url'), 
                    data: formdata 
                });
                if (!result.confirmed || !result.data) return;
                const res = result.data;
                if (res.status_code !== 1) {
                    ToastHelper.showError();
                    validator.showErrors(result.errors);
                    return;
                }
                ToastHelper.showSuccess();
                FormValidateLoader.savedNext(event, {
                    url_save: frm$.data('url-list'),
                    url_add_another: frm$.data('url-add'),
                    url_continue_editing: frm$.data('url-detail').replace('__pk__', res.id),
                });
            }
        }
    )
})