$(document).ready(function () {
    const frm$ = $('#frm_modal_attribute_value')
    const tbl$ = $('#datatables-attribute-values');
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
                if (!result.confirmed){
                    un_formart_price = formatPriceOnInput(price)
                    priceInput.val(un_formart_price)
                    return;
                }
                if (result.data.status_code !== 1) {
                    ToastHelper.showError();
                    validator.showErrors(result.errors);
                    return;
                }
                ToastHelper.showSuccess();
                modal.hide();
                form.reset();
                tbl$.DataTable().ajax.reload();
            }
        }
    )
})