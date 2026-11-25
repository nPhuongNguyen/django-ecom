$(document).ready(function () {
    const frm$ = $('#frm_create_product')
    const uppyInstance  = UppyUploader.init('#image_product', null, {
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 10 * 1024 * 1024,
                maxNumberOfFiles: 1,
            },
        },
    });
    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();

                const check_confirmed = await SweetAlertHelper.confirmSave({});
                if (!check_confirmed) return;

                try {
                    MyLoading.show();

                    const formdata = FormValidateLoader.formData(frm$, {
                        name_type_list: ["attributes"]
                    });

                    const changed_img = UppyUploader.hasChanged(uppyInstance);
                    let hasError = false; 

                    if (changed_img) {
                        const files = UppyUploader.getFiles(uppyInstance);
                        if (files.length > 0) {
                            const formDataImage = new FormData();
                            files.forEach(file => formDataImage.append('list_image', file.data));
                            
                            const api_upload = frm$.data('url-upload');
                            try {
                                const result_api_image = await CallApi.request({
                                    url: api_upload,
                                    method: 'POST',
                                    data: formDataImage
                                });

                                if (result_api_image.status_code !== 1) {
                                    SweetAlertHelper.NotiError({
                                        text: result_api_image.message || 'Lỗi tải ảnh lên'
                                    });
                                    hasError = true;
                                } else {
                                    formdata['img'] = result_api_image.data.list_img;
                                }
                            } catch {
                                SweetAlertHelper.NotiError();
                                hasError = true;
                            }
                        } else {
                            formdata['img'] = ""; 
                        }
                    }
                    if (hasError) return;
                    const result_api_create_product = await CallApi.request({
                        url: frm$.data('url'),
                        method: 'POST',
                        data: formdata
                    });

                    if (result_api_create_product.status_code !== 1) {
                        ToastHelper.showError();
                        validator.showErrors(result_api_create_product.errors);
                        return;
                    }

                    ToastHelper.showSuccess();
                    FormValidateLoader.savedNext(event, {
                        url_save: frm$.data('url-list'),
                        url_add_another: frm$.data('url-add'),
                        url_continue_editing: frm$.data('url-detail').replace('__pk__', result_api_create_product.data.id),
                    });

                } catch (error) {
                    SweetAlertHelper.NotiError();
                } finally {
                    MyLoading.close();
                }
            }
        }
    );
    
    const selectCategory$ = $('#inp_select_category');
    Select2Helper.init(selectCategory$, {
        url: selectCategory$.data('url'),            
        valueField: 'id',       
        textField: 'name'   
    });

    const selectAttribute$ = $('#inp_select_attribute');
    Select2Helper.init(selectAttribute$, {
        url: selectAttribute$.data('url'),            
        valueField: 'id',       
        textField: 'name',
        multiple: true   
    });
});