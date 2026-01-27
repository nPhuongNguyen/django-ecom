$(document).ready(function () {
    const frm$ = $('#frm_modal_attribute_value');
    const modalEl = document.querySelector('#modal_attribute_value');
    const modal = KTModal.getInstance(modalEl);
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
                if (result.data.status_code !== 1) {
                    ToastHelper.showError();
                    validator.showErrors(result.errors);
                    return;
                }
                ToastHelper.showSuccess();
                modal.hide();
                form.reset();
                window.location.reload();
            }
        }
    )
    const selectAttributeValue$ = $('#inp_select_attribute_value');
    const apiURL$ = selectAttributeValue$.data('url');
    Select2Helper.init(selectAttributeValue$, {
        url: apiURL$,            
        valueField: 'id',       
        textField: 'name',
        multiple: true   
    });
})