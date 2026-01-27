$(document).ready(function () {
    const tbl$ = $('#datatables-products');
    const dtb$ = DataTableLoader.init(tbl$, {
        ajax: {
            url: tbl$.data('url'),
            headers: {
                'Token': AuthStorage.getToken(),
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
            const check_confirmed = await SweetAlertHelper.confirmSave({});
            if (!check_confirmed) return;
            const result_ai = await CallApi.request({
                url: tbl$.data('url-change-status').replaceAll('__pk__', id),
                method: 'POST',
            });
            MyLoading.show();
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
                tbl$.DataTable().ajax.reload();
            }
        },
        selectRow: 'multi',
        selectRowRender: (select_info$) => {
            const btnDestroy$ = $(`<button class="kt-btn kt-btn-destructive">Delete selected</button>`);
            select_info$.append(btnDestroy$);

            btnDestroy$.on('click', async function () {
                const id_selecteds = DataTableLoader.get_selected_row_data(tbl$).map(row => row.id);
                if (id_selecteds.length === 0) return;
                MyLoading.show();
                try{
                    const check_confirmed = await SweetAlertHelper.confirmDelete({});
                    if (!check_confirmed) return;
                    const result = await CallApi.request({
                        url: tbl$.data('url-delete'),
                        method: 'POST',
                        params: { 'id[]': id_selecteds },
                    });
                    if (result == null){
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
    DataTableLoader.init_filter_is_status(tbl$);
});