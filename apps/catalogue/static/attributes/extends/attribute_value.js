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
                result = await SweetAlertHelper.confirmSave({ 
                    url: frm$.data('url'), 
                    data: formdata 
                });
                if(result){
                    if (result.cancelled){
                        return;
                    }
                    else if (result.status_code !== 1) {
                        ToastHelper.showError();
                        validator.showErrors(result.errors);
                    }
                    else {
                        ToastHelper.showSuccess();
                        modal.hide();
                        setTimeout(() => {
                            window.location.reload();
                        }, 1200);
                        return;
                    }
                }
                else {
                    SweetAlertHelper.NotiError();
                }
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