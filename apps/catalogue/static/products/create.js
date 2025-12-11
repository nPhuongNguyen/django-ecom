$(document).ready(function () {
    const frm$ = $('#frm_create_product')
    // const img = "http://localhost:9001/sys/django_ecom/ecom/product/Ảnh chụp màn hình 2025-11-27 102114.png;http://localhost:9001/sys/django_ecom/ecom/product/Ảnh chụp màn hình 2025-12-03 104707.png";
    const uppyInstance  = UppyUploader.init('#image_product', null, {
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
                let result = null;
                if (changed) {
                    if (files.length > 0) {
                        const formDataImage = new FormData();
                        files.forEach(file => formDataImage.append('list_image', file.data));
                        const api_upload = frm$.data('url-upload');
                        const check_sw2_alret = await SweetAlertHelper.confirmSave();
                        if (check_sw2_alret.cancelled){
                            return;
                        }
                        if(check_sw2_alret.confirmed){
                            try{
                                MyLoading.show();
                                await new Promise(resolve => setTimeout(resolve, 1500));
                                result_api_image = await CallApi.request({
                                    url: api_upload,
                                    method: 'POST',
                                    data: formDataImage
                                })
                                if(result_api_image){
                                    if(result_api_image.status_code !== 1){
                                        SweetAlertHelper.NotiError({
                                            text: result_api_image.message
                                        });
                                        return;
                                    }else{
                                        formdata['img'] = result_api_image.data.list_img
                                        result = await CallApi.request({
                                            url: frm$.data('url'),
                                            method: 'POST',
                                            data: formdata
                                        })
                                    }
                                }else{
                                    SweetAlertHelper.NotiError();
                                    return;
                                }
                            }
                            finally{
                                MyLoading.close();
                            }
                        }
                    }
                    else{
                        formdata['img'] = "";
                    }
                }
                else{
                    result = await SweetAlertHelper.confirmSave({ 
                        url: frm$.data('url'), 
                        data: formdata 
                    });
                }
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
                        FormValidateLoader.savedNext(event, {
                            url_save: frm$.data('url-list'),
                            url_add_another: frm$.data('url-add'),
                            url_continue_editing: frm$.data('url-detail').replace('__slug__', result.data.slug),
                        });
                    }
                }
                else {
                    SweetAlertHelper.NotiError();
                }
            }
        }
    );
});