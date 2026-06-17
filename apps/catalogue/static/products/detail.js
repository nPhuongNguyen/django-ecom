$(document).ready(async function () {
    const frm$ = $('#frm_detail_product');

    const product$ = await CallApi.request(
        {
            url: frm$.data('url'),
            method: 'GET'
        })
    const form = FormValidateLoader.fillForm(frm$, product$.data)

    const uppyInstance  = UppyUploader.init('#image_product',  product$.data.img, {
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 10 * 1024 * 1024,
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

    const validator = FormValidateLoader.init(
        frm$,
        {
            submitHandler: async function (form, event) {
                event.preventDefault();
                const formdata = FormValidateLoader.formData(frm$);
                const changed_img = UppyUploader.hasChanged(uppyInstance);
                const check_confirmed = await SweetAlertHelper.confirmSave({});
                MyLoading.show();
                try{
                    if (changed_img) {
                        const files = UppyUploader.getFiles(uppyInstance);
                        if (files.length > 0) {
                            const formDataImage = new FormData();
                            files.forEach(file => formDataImage.append('list_image', file.data));
                            const api_upload = frm$.data('url-upload');
                            const result_api_image = await CallApi.request({
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
                                }
                            }else{
                                SweetAlertHelper.NotiError();
                                return;
                            }
                        }
                        else{
                            formdata['img'] = "";
                        }
                    }
                    const result_api = await CallApi.request({
                        url: frm$.data('url-update'),
                        method: 'POST',
                        data: formdata
                    })
                    if (result_api){
                        if (result_api.status_code !== 1) {
                            ToastHelper.showError();
                            validator.showErrors(result_api.errors);
                            return;
                        }else{
                            ToastHelper.showSuccess();
                            FormValidateLoader.savedNext(event, {
                                url_save: frm$.data('url-list'),
                                url_add_another: frm$.data('url-add'),
                                url_continue_editing: frm$.data('url-detail'),
                            });
                        }
                    }else{
                        ToastHelper.showError();
                        return;
                    } 
                }finally{
                    MyLoading.close();
                }
            },
        },
        frm$.find('button.btn-delete').on('click', async function(){
            if(frm$.data('pk') === null){
                ToastHelper.showError();
                return;
            }
            const confirmed =  await SweetAlertHelper.confirmDelete({});
            if (!confirmed){
                return;
            }
            MyLoading.show();
            try{
                const result_api = await CallApi.request({
                    url: frm$.data('url-delete'),
                    method: 'POST',
                    params: {'id[]': frm$.data('pk')}
                });
                if (result_api == null){
                    ToastHelper.showError();
                    return;
                }
                if (result_api.status_code !== 1){
                    ToastHelper.showError();
                    return;
                }
                ToastHelper.showSuccess();
                window.location.href = frm$.data('url-list');
            }finally {
                MyLoading.close();
            }
        })
    );
})