$(document).ready(function () {
    const tbl$ = $('#datatables-products');
    const dtb$ = DataTableLoader.init(tbl$, {
        ajax: {
            url: tbl$.data('url'),
            headers: {
                'Token': AuthStorage.getToken("Token"),
            },
            ...DataTableLoader.ajax_base(),
        },
        orderCellsTop: true,
        columns: [
            { 
                data: 'name',
                name: 'name',
                allowHtml: true,
                render(data, type, row) {
                    const url = tbl$.data('url-detail').replaceAll('__slug__', row['slug'] || '');
                    return `<a class="kt-link kt-link-underline" href="${url}">${data || '-'}</a>`;
                }
            },
            { 
                data: 'slug',
                name: 'slug',
                orderable: false,
                render(data, type, row) {
                    return data || '-';
                }

            },
            { 
                data: 'description',
                name: 'description',
                orderable: false,
                render(data, type, row) {
                    return data || '-';
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
                try {
                    const result_ai = await CallApi.request({
                        url: tbl$.data('url-change-status').replaceAll('__pk__', id),
                        method: 'POST',
                    });
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
        selectRowRender: (actionContainer, selectedRows, table$) => {
            const btnDestroy$ = $(`
                <button class="kt-btn kt-btn-destructive flex items-center gap-2">
                    <i class="ki-filled ki-trash"></i>
                    Delete selected
                </button>
            `);
            actionContainer.append(btnDestroy$);
            btnDestroy$.on('click', async function () {
                const id_selecteds = selectedRows.map(r => r.id);
                if (id_selecteds.length === 0) return;
                const check_confirmed = await SweetAlertHelper.confirmDelete({});
                if (!check_confirmed) return;
                    MyLoading.show();
                try{
                    const result = await CallApi.request({
                        url: tbl$.data('url-delete'),
                        method: 'POST',
                        params: { 'id[]': id_selecteds },
                    });
                    if (result === null){
                        ToastHelper.showError();
                        return;
                    }
                    if (result.status_code !== 1){
                        ToastHelper.showError();
                        return;
                    }
                    ToastHelper.showSuccess();
                    tbl$.DataTable().ajax.reload();
                }finally{
                    MyLoading.close();
                }
            });
        },
    });
    // DataTableLoader.initAddButton(tbl$, 'Thêm mới', () => {
    //     const addUrl = tbl$.data('url-add');
    //     if (addUrl) {
    //         window.location.href = addUrl;
    //     }
    // });
    DataTableLoader.init_filter_is_status(tbl$);
});