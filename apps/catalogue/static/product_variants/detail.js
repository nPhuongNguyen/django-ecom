async function getProductVariant(url) {
    const result = await CallApi.request({
        url,
        method: 'GET'
    });
    if (result.status_code !== 1) {
        throw new Error(result.message);
    }
    return result.data;
}
function initProduct(product) {
    const selectProduct = $('#inp_select_product');

    Select2Helper.init(selectProduct, {
        url: selectProduct.data('url'),
        valueField: 'id',
        textField: 'name'
    });

    if (product) {
        const option = new Option(
            product.name,
            product.id,
            true,
            true
        );

        selectProduct.append(option).trigger('change');
    }
}

function initUppy(imageUrl = '') {
    return UppyUploader.init('#image_product_variant', imageUrl, {
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 10 * 1024 * 1024,
                maxNumberOfFiles: 1,
            },
        },
    });
}


$(document).ready(async function () {
    const frm$ = $('#frm_detail_product_variant');
    const productVariant =
        await getProductVariant(
            frm$.data('url')
        );
    FormValidateLoader.fillForm(
        frm$,
        productVariant
    );
    const uppyInstance = initUppy(productVariant.img);
    initProduct(
        productVariant.product
    );

    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function(form, event){
                event.preventDefault();
                const formdata = FormValidateLoader.formData(frm$);
                const files = UppyUploader.getFiles(uppyInstance);
                const changed = UppyUploader.hasChanged(uppyInstance);
                if (changed) {
                    const check_sw2_alret = await SweetAlertHelper.confirmSave();
                    if (!check_sw2_alret.confirmed) return
                    if (files.length > 0) {
                        try{
                            const formDataImage = new FormData();
                            files.forEach(file => formDataImage.append('list_image', file.data));
                            const api_upload = frm$.data('url-upload');
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
                }
                else{
                    formdata['img'] = "";
                }
                try{
                    const result = await CallApi.request({
                        url: frm$.data('url-update'),
                        method: 'POST',
                        data: formdata
                    })
                    if (result.status_code !== 1){
                        ToastHelper.showError();
                        validator.showErrors(result.errors);
                        return;
                    }
                    ToastHelper.showSuccess();
                    FormValidateLoader.savedNext(event, {
                        url_save: frm$.data('url-list'),
                        url_add_another: frm$.data('url-add'),
                        url_continue_editing: frm$.data('url-detail'),
                    });
                }catch{
                    SweetAlertHelper.NotiError();
                    return;
                }
            }
        }
    )
})