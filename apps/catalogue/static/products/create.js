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
                const formdata = FormValidateLoader.formData(frm$);
                let dataAttributes = [];
                if (formdata.attributes) {
                    dataAttributes = formdata.attributes;
                    delete formdata.attributes;
                }
                const changed = UppyUploader.hasChanged(uppyInstance);
                const check_confirmed = await SweetAlertHelper.confirmSave({});
                if (!check_confirmed) return;
                MyLoading.show();
                try {
                    if (changed) {
                        const files = UppyUploader.getFiles(uppyInstance);
                        if (files.length > 0) {
                            const formDataImage = new FormData();
                            files.forEach(file => formDataImage.append('list_image', file.data));
                            const api_upload = frm$.data('url-upload');
                            try{
                                const result_api_image = await CallApi.request({
                                url: api_upload,
                                method: 'POST',
                                data: formDataImage
                                })
                                if(result_api_image.status_code !== 1){
                                    SweetAlertHelper.NotiError({
                                        text: result_api_image.message
                                    });
                                    return;
                                }else{
                                    formdata['img'] = result_api_image.data.list_img
                                }
                            }catch{
                                SweetAlertHelper.NotiError();
                                return;
                            }
                        }
                        else{
                            formdata['img'] = "";
                        }
                    }
                    try{
                        const resultProduct  = await CallApi.request({
                        url: frm$.data('url'),
                        method: 'POST',
                        data: formdata
                        })
                        if (resultProduct .status_code !== 1) {
                            ToastHelper.showError();
                            validator.showErrors(resultProduct.errors);
                            return;
                        }
                        const productId = resultProduct.data.id;
                        if (dataAttributes.length > 0){
                            const resultAttribute = await CallApi.request({
                            url: frm$.data('url-add-product-attribute'),
                            method: 'POST',
                            data: {
                                product: productId,
                                attributes: dataAttributes
                            }
                            })
                            if (resultAttribute.status_code !== 1) {
                                ToastHelper.showError();
                                validator.showErrors(result_api.errors);
                                return;
                            }
                        }
                        ToastHelper.showSuccess();
                        FormValidateLoader.savedNext(event, {
                            url_save: frm$.data('url-list'),
                            url_add_another: frm$.data('url-add'),
                            url_continue_editing: frm$.data('url-detail').replace('__pk__', productId),
                        });
                    }catch{
                        SweetAlertHelper.NotiError();
                        return;
                    }
                }finally {
                    MyLoading.close();
                }
            }
        },
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