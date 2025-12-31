$(document).ready(function () {

    const frm$ = $('#frm_create_product_variant')

    const selectProduct$ = $('#inp_select_product');
    const apiURL$ = selectProduct$.data('url');
    Select2Helper.init(selectProduct$, {
        url: apiURL$,            
        valueField: 'id',       
        textField: 'name'   
    });
    const uppyInstance  = UppyUploader.init('#image_product_variant', null, {
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 500 * 1024,
                maxNumberOfFiles: 1,
            },
        },
    });


    const priceInput = frm$.find("#inp_price");
    function formatPriceOnInput(value) {
        if (!value) return "";

        // đổi về dạng số với dấu phẩy
        value = value.toString().replace(".", ",");

        // tách phần nguyên + thập phân
        let parts = value.split(",");

        // format phần nguyên: 100000 → 100.000
        parts[0] = Number(parts[0]).toLocaleString("vi-VN");

        return parts.join(",");
    }
    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();
                let price = priceInput.val();
                price = price.replace(/\./g, "").replace(",", ".");
                priceInput.val(price);
                const formdata = FormValidateLoader.formData(frm$);
                const changed = UppyUploader.hasChanged(uppyInstance);
                let result = null;
                if (changed) {
                    const files = UppyUploader.getFiles(uppyInstance);
                    let result_api_image = null;
                    if (files.length > 0) {
                        const formDataImage = new FormData();
                        files.forEach(file => formDataImage.append('list_image', file.data));
                        const api_upload = frm$.data('url-upload');
                        const check_sw2_alret = await SweetAlertHelper.confirmSave();
                        if (check_sw2_alret.cancelled){
                            un_formart_price = formatPriceOnInput(price)
                            priceInput.val(un_formart_price)
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
                        un_formart_price = formatPriceOnInput(price)
                        priceInput.val(un_formart_price)
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
                            url_continue_editing: frm$.data('url-detail').replace('__pk__', result.data.id),
                        });
                    }
                }
                else {
                    SweetAlertHelper.NotiError();
                }
            }
        },
    )
})