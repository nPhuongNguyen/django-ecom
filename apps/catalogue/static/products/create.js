$(document).ready(function () {
    const frm$ = $('#frm_create_product')
    const img = "http://localhost:9001/sys/django_ecom/ecom/product/Ảnh chụp màn hình 2025-11-27 102114.png;http://localhost:9001/sys/django_ecom/ecom/product/Ảnh chụp màn hình 2025-12-03 104707.png";
    const uppyInstance  = UppyUploader.init('#image_product', img, {
        endpoint: '/upload/logo',
        fieldName: 'logo',
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 500 * 1024,
                maxNumberOfFiles: 5,
            },
        },
    });
    
    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();
                const formdata = FormValidateLoader.formData(frm$);
                const files = UppyUploader.getFiles(uppyInstance);
                const changed = UppyUploader.hasChanged(uppyInstance);
                console.log('changed:', changed);
                if (changed) {
                    if (files.length > 0) {
                        const formDataImage = new FormData();
                        files.forEach(file => formDataImage.append('list_image', file.data));
                        console.log('Files to upload:', files);
                        const api_upload = frm$.data('url-upload');
                        const upload_result = await CallApi.request({
                            url: api_upload,
                            method: 'POST',
                            data: formDataImage,
                        });
                        if (upload_result && upload_result.status_code === 1) {
                            formdata['image'] = upload_result.data.list_img
                        }
                    }else{
                        formdata['image'] = "hihihi";
                    }
                }
                console.log('Final form data to submit:', formdata);
                return;
                const result = await SweetAlertHelper.confirmSave({ 
                    url: frm$.data('url'), 
                    data: formdata 
                });

            }
        }
    );
});