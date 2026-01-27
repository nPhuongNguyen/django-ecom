$(document).ready(function () {
    const tbl$ = $('#datatables-product-variants');
    const dtb$ = DataTableLoader.init(tbl$, {
        ajax: {
            url: tbl$.data('url-variant'),
            headers: {
                'Token': AuthStorage.getToken(),
            },
            ...DataTableLoader.ajax_base(),
        },
        ordering: true,
        orderCellsTop: true,
        order: [[0, 'asc']],
        columns: [
            { 
                data: 'name',
                name: 'name',
                orderable: false,
                allowHtml: true,
                render(data, type, row) {
                    const url = tbl$.data('url-detail-variant').replaceAll('__pk__', row['id'] || '');
                    return `<a class="kt-link kt-link-underline" href="${url}">${data || '-'}</a>`;
                }
            },
            { 
                data: 'sku',
                name: 'sku',
                orderable: false,
                render(data, type, row) {
                    return data || '-';
                }

            },
            { 
                data: 'stock_qty',
                name: 'stock_qty',
                orderable: false,
                render(data, type, row) {
                    return data ?? '-';
                }
            },
            DataTableLoader.col_is_price(),  
            DataTableLoader.col_is_status({ useToggle: true }),
        ],
        ontoggleActive: async (id)=>{
            try{
                const check_confirmed = await SweetAlertHelper.confirmSave({});
                if (!check_confirmed) return;
                MyLoading.show();
                const result_ai = await CallApi.request({
                    url: tbl$.data('url-change-status-variant').replaceAll('__pk__', id),
                    method: 'POST',
                });
                try {
                    if (result_ai == null){
                        ToastHelper.showError();
                        return;
                    }
                    if (result_ai.status_code !== 1){
                        ToastHelper.showError();
                        return;
                    }
                    ToastHelper.showSuccess();
                }
                finally{
                    MyLoading.close();
                }
            }finally{
                tbl$.DataTable().ajax.reload();
            }
        },
        selectRow: 'multi',
        selectRowRender: (select_info$) => {
            const btnDestroy$ = $(`<button class="kt-btn kt-btn-destructive">Delete selected</button>`);
            select_info$.append(btnDestroy$);
            btnDestroy$.on('click', async function (event) {
                event.preventDefault()
                const id_selecteds$ = DataTableLoader.get_selected_row_data(tbl$).map(row => row.id);
                if (id_selecteds$.length === 0) return;
                const check_confirmed = await SweetAlertHelper.confirmDelete({});
                if (!check_confirmed) return;
                const result_api = await CallApi.request({
                    url: tbl$.data('url-delete-variant'),
                    method: 'POST',
                    params: {'id[]': id_selecteds$}
                });
                if (result_api){
                    if (result_api.status_code !==1){
                        ToastHelper.showError();
                        return;
                    }
                    ToastHelper.showSuccess();
                    tbl$.DataTable().ajax.reload();
                }else{
                    SweetAlertHelper.NotiError();
                    return;
                }
            });
        },
    });
    DataTableLoader.init_filter_is_status(tbl$)
    //Add Product Variant
    const frm$ = $('#frm_modal_variant')
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
    const modalEl = document.querySelector('#modal_product_variant');
    const modal = KTModal.getInstance(modalEl);
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
                const check_confirmed = await SweetAlertHelper.confirmSave({});
                if (!check_confirmed) {
                    un_formart_price = formatPriceOnInput(price)
                    priceInput.val(un_formart_price)
                    return;
                }
                MyLoading.show()
                try{
                    if (changed) {
                        const files = UppyUploader.getFiles(uppyInstance);
                        if (files.length > 0) {
                            const formDataImage = new FormData();
                            files.forEach(file => formDataImage.append('list_image', file.data));
                            const api_upload = frm$.data('url-upload-variant');
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
                    try{
                        const result_api = await CallApi.request({
                            url: frm$.data('url-create-variant'),
                            method: 'POST',
                            data: formdata
                        })
                        if (result_api.status_code !== 1) {
                            ToastHelper.showError();
                            validator.showErrors(result_api.errors);
                            return;
                        }
                    }finally{
                        un_formart_price = formatPriceOnInput(price)
                        priceInput.val(un_formart_price)
                    }
                    ToastHelper.showSuccess();
                    modal.hide();
                    form.reset();
                    tbl$.DataTable().ajax.reload();
                }finally{
                    MyLoading.close();
                }
            }
        },
    )
});