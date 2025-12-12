$(document).ready(async function () {
    const frm$ = $('#frm_detail_product');
    const check_image$ = $('#check_image');
    const check_image_val$ = check_image$.val();
    let image$ = null
    if(check_image$ && check_image_val$){
        image$ = check_image$.val()
    }
    const uppyInstance  = UppyUploader.init('#image_product', image$, {
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 500 * 1024,
                maxNumberOfFiles: 1,
            },
        },
    });


    const selectCategory$ = $('#inp_select_category');
    const apiURL$ = selectCategory$.data('url');
    Select2Helper.init(selectCategory$, {
        url: apiURL$,            
        valueField: 'id',       
        textField: 'name'   
    });
    let result = null;
    const check_id_product$ = $('#id_product');
    const check_val$ = check_id_product$.val();
    let id_product$ = null;
    if(check_id_product$ && check_val$){
        id_product$ = check_val$
    }

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
    const initialPrice = priceInput.val();
    if (initialPrice) {
        priceInput.val(formatPriceOnInput(initialPrice));
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
                console.log('formdata',formdata);
                const files = UppyUploader.getFiles(uppyInstance);
                const changed = UppyUploader.hasChanged(uppyInstance);
                let result_api_image = null;
                if (changed) {
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
                        if(id_product$ == null){
                            ToastHelper.showError();
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
                                            url: frm$.data('url').replace('__pk__', id_product$),
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
                        url: frm$.data('url').replace('__pk__', id_product$),
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
                            url_continue_editing: frm$.data('url-detail').replace('__slug__', result.data.slug),
                        });
                    }
                }
                else {
                    SweetAlertHelper.NotiError();
                }
            },
        },
        frm$.find('button.btn-delete').on('click', async function(){
            if(id_product$ == null){
                ToastHelper.showError();
                return;
            }
            const result = await SweetAlertHelper.confirmDelete({
                url: frm$.data('url-delete'),
                params: {'id[]': id_product$}
            });
            if(result){
                if(result.cancelled){
                    return;
                }else if(result.status_code !== 1){
                    ToastHelper.showError();
                }else{
                    ToastHelper.showSuccess();
                    await new Promise(resolve => {
                        setTimeout(() => {
                            window.location.href = frm$.data('url-list');
                            resolve();
                        }, 1500);
                    });
                }
            }
            else{
                SweetAlertHelper.NotiError();
            }
        })
    );
})