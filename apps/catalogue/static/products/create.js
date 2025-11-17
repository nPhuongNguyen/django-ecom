$(document).ready(function () {
    const frm$ = $('#frm_create_product')
    FilePondHelper.registerPlugins();
    let selectedFile = null;

    FilePondHelper.init("#inp_image", (file) => {
        selectedFile = file;
    });

    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: function (form, event) {
                event.preventDefault();
                const data = FormValidateLoader.formData(frm$);
                data.image = selectedFile
                SweetAlertHelper.confirmSave({ 
                    url: frm$.data('url'), 
                    data: data 
                });
            }
        }
    );
});

