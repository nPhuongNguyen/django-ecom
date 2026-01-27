$(document).ready(async function () {
    const frm$ = $('#frm_detail_attribute');
    let id_attribute$ = null;
    const check_id_attribute$ = frm$.find('#id_attribute');
    const check_val$ = check_id_attribute$.val();
    if(check_id_attribute$ && check_val$){
        id_attribute$ = check_val$
    }
    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();
                const formdata = FormValidateLoader.formData(frm$);
               
                const result = await SweetAlertHelper.confirmSave({
                    url: frm$.data('url').replace('__pk__', id_attribute$),
                    data: formdata
                });
                if (!result.confirmed || !result.data) return;
                const res = result.data;
                if (res.status_code !== 1){
                    ToastHelper.showError();
                    validator.showErrors(result.errors || {});
                    return;
                }
                ToastHelper.showSuccess();
                FormValidateLoader.savedNext(event, {
                    url_save: frm$.data('url-list'),
                    url_add_another: frm$.data('url-add'),
                    url_continue_editing: frm$.data('url-detail').replace('__pk__', res.data.id),
                });
            },
        },
        frm$.find('button.btn-delete').on('click', async function(){
            if(id_attribute$ == null){
                ToastHelper.showError();
                return;
            }
            const result = await SweetAlertHelper.confirmDelete({
                url: frm$.data('url-delete'),
                params: {'id[]': id_attribute$}
            });
            if (!result.confirmed) return;
            if (result.data.status_code !== 1){
                ToastHelper.showError();
                return;
            }
            window.location.href = frm$.data('url-list');
        })
    );
})