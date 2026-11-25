async function getProduct(url) {
    const result = await CallApi.request({
        url,
        method: 'GET'
    });
    if (result.status_code !== 1) {
        SweetAlertHelper.NotiError();
    }
    return result.data;
}
function initUppy(imageUrl = '') {
    return UppyUploader.init('#image_product', imageUrl, {
        uppyOptions: {
            restrictions: {
                allowedFileTypes: ['.jpg', '.jpeg', '.png'],
                maxFileSize: 10 * 1024 * 1024,
                maxNumberOfFiles: 1,
            },
        },
    });
}
function initCategory(category) {
    const selectCategory = $('#inp_select_category');
    Select2Helper.init(selectCategory, {
        url: selectCategory.data('url'),
        valueField: 'id',
        textField: 'name'
    });
    if (category) {
        const option = new Option(
            category.name,
            category.id,
            true,
            true
        );
        selectCategory.append(option).trigger('change');
    }
}
async function uploadImage(frm, uppyInstance) {
    if (!UppyUploader.hasChanged(uppyInstance)) {
        return null;
    }
    const files = UppyUploader.getFiles(uppyInstance);
    // user xóa toàn bộ ảnh
    if (files.length === 0) {
        return "";
    }
    const formDataImage = new FormData();
    files.forEach(file => {
        formDataImage.append(
            'list_image',
            file.data
        );
    });
    const result = await CallApi.request({
        url: frm.data('url-upload'),
        method: 'POST',
        data: formDataImage
    });
    if (result.status_code !== 1) {
        SweetAlertHelper.NotiError();
    }
    return result.data.list_img;
}

async function deleteProduct(productId, deleteUrl, listUrl) {
    const confirmed = await SweetAlertHelper.confirmDelete({});
    if (!confirmed) return;
    try {
        MyLoading.show();
        const result_api_delete = await CallApi.request({
            url: deleteUrl,
            method: 'POST',
            params: {
                'id[]': productId
            }
        });

        if (result_api_delete.status_code !== 1) {
            SweetAlertHelper.NotiError({
                text: result_api_delete.message
            });
            return;
        }
        ToastHelper.showSuccess();
        setTimeout(() => {
            window.location.href = listUrl;
        }, 1500);
    } catch{
        ToastHelper.showError();
    } finally {
        MyLoading.close();
    }
}

$(document).ready(async function () {
    const frm = $('#frm_detail_product');
    const product = await getProduct(frm.data('url'));
    FormValidateLoader.fillForm(frm, product);
    const uppyInstance = initUppy(product.img);
    initCategory(product.category);
    const validator = FormValidateLoader.init(
        frm,
        {
            submitHandler:async function (form, event) {
                event.preventDefault();
                const confirmed = await SweetAlertHelper.confirmSave({});
                if (!confirmed) return;
                try {
                    MyLoading.show();
                    const formData = FormValidateLoader.formData(frm);
                    const imageResult = await uploadImage(frm, uppyInstance);
                    if (imageResult !== null) {
                        formData.img = imageResult;
                    }
                    const result = await CallApi.request({
                        url: frm.data('url-update'),
                        method: 'POST',
                        data: formData
                    });
                    if (result.status_code !== 1) {
                        ToastHelper.showError();
                        validator.showErrors(
                            result.errors
                        );
                        return;
                    }
                    ToastHelper.showSuccess();
                    FormValidateLoader.savedNext(event, {
                        url_save: frm.data('url-list'),
                        url_add_another: frm.data('url-add'),
                        url_continue_editing: frm.data('url-detail'),
                    });
                } catch{
                    SweetAlertHelper.NotiError();

                } finally {
                    MyLoading.close();
                }
            }
        }
    );
    frm.find('.btn-delete').on('click', () => deleteProduct(product.id, frm.data('url-delete'), frm.data('url-list')));
});