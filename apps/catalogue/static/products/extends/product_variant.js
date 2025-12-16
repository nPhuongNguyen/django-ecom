$(document).ready(function () {
    frm_model_variant$ = $('#frm_modal_variant');
    frm_product_variant$ = $('#frm_product_variant');
    check_image$ = $('#check_image_product_variant').val();
    btnEdit$ = $('.btn-edit-variant');
    btnDelete$ = $('.btn-delete-variant');
    const modalEl = document.querySelector('#modal_variant');
    const modal = KTModal.getInstance(modalEl);
    
    const uppyInstanceProductVariantInput  = UppyUploader.init('#image_product_variant_input', null, {
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 500 * 1024,
                maxNumberOfFiles: 1,
            },
        },
    });
    frm_product_variant$
    .find('.image-product-variant')
    .each(function () {
        const $el = $(this);
        const variantId = $el.data('variant-id');

        const checkImage = frm_product_variant$
            .find(`.check-image-product-variant[data-variant-id="${variantId}"]`)
            .val() || null;

        UppyUploader.init(this, checkImage, {
            uppyOptions: {
                restrictions: {
                    allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                    maxFileSize: 500 * 1024,
                    maxNumberOfFiles: 1,
                },
            },
        });
    });

    const priceInput = frm_model_variant$.find("#inp_price");
    function formatPriceOnInput(value) {
        if (!value) return "";

        // đổi về dạng số với dấu phẩy
        value = value.toString().replace(".", ",");

        // tách phần nguyên + thập phân
        let parts = value.split(",");

        // format phần nguyên: 100000 → 100.000
        parts[0] = Number(parts[0]).toLocaleString("vi-VN");

        return parts.join(",");
    };
    const validator = FormValidateLoader.init(
        frm_model_variant$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();
                let price = priceInput.val();
                price = price.replace(/\./g, "").replace(",", ".");
                priceInput.val(price);
                api_upload = frm_model_variant$.data('url-upload');
                const formdata = FormValidateLoader.formData(frm_model_variant$);
                const changed = UppyUploader.hasChanged(uppyInstanceProductVariantInput);
                if(changed){
                    const files = UppyUploader.getFiles(uppyInstanceProductVariantInput);
                    let result_api_image = null;
                    if(files.length > 0){
                        const formDataImage = new FormData();
                        files.forEach(file => formDataImage.append('list_image', file.data));
                        const api_upload = frm_model_variant$.data('url-upload');
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
                                            url: frm_model_variant$.data('url'),
                                            method: 'POST',
                                            data: formdata
                                        })
                                    }
                                }else{
                                    SweetAlertHelper.NotiError();
                                    return;
                                }
                            }finally{
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
                        url: frm_model_variant$.data('url'), 
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
    btnEdit$.click(async function(){
        console.log("btn edit");
    });
    btnDelete$.click(async function(){
        const result = await SweetAlertHelper.confirmSave({
            url: frm_product_variant$.data('url-delete'),
            params: {
                'id[]':$(this).data('id')
            }
        });
        if(result.cancelled){
            return;
        }
        if(result){
            if(result.status_code !==1){
                ToastHelper.showError();
                return;
            }else{
                ToastHelper.showSuccess();
                setTimeout(() => {
                    window.location.reload();
                }, 1200);
                return;
            }
        }
        else{
            SweetAlertHelper.NotiError();
            return;
        }
    });

})