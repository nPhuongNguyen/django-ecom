$(document).ready(function () {
    const frm$ = $('#frm_create_product')
    FilePondHelper.registerPlugins();

    const pond = FilePondHelper.init("#inp_image");
    const hidden$ = frm$.find('input[name="image"]');
    pond.on('addfile', () => {
        hidden$.val('has-file'); 
        hidden$.valid();   
        validator.showErrors({image: ''});  
    });
    pond.on('removefile', () => {
        hidden$.val('');
        hidden$.valid();
        validator.showErrors({image: ''});
    });

    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();
                // const data = FormValidateLoader.formData(frm$);
                const data = new FormData(frm$[0]);
                data.delete('filepond');
                data.delete('image');
                
                if (pond && pond.getFiles().length > 0) {
                    const file = pond.getFiles()[0].file;
                    data.append('image', file);
                } else {
                    data.delete('image');
                }
                
                const result = await SweetAlertHelper.confirmSave({ 
                    url: frm$.data('url'), 
                    data: data 
                });
                
                if (result && result.status === 'error') {
                    console.log(result.data);
                    if (typeof result.data === 'object') {
                        validator.showErrors(result.data)
                    }
                    return;
                }
                else if (result && result.status == 'success'){
                    console.log(result.data);
                    return;
                }
            }
        }
    );
});


