$(document).ready(function () {
    const tbl$ = $('#datatables-attributes');
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
                orderable: false,
                render(data, type, row) {
                    const url = tbl$.data('url-detail').replaceAll('__pk__', row['id'] || '');
                    return `<a class="kt-link kt-link-underline" href="${url}">${data || '-'}</a>`;
                }
            },
            DataTableLoader.col_is_status({ useToggle: true }),
        ],
        ontoggleActive: async (id)=>{
            const result = await SweetAlertHelper.confirmSave({
                url: tbl$.data('url-change-status').replaceAll('__pk__', id),
                method: 'POST',
            });
            try{
                if (result){
                    if (result.cancelled){
                        console.log("User cancelled");
                    }
                    else if (result.status_code !==1){
                        ToastHelper.showError();
                    }
                    else{
                        ToastHelper.showSuccess();
                    }
                }
            }
            finally{
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

                const result = await SweetAlertHelper.confirmDelete({
                    url: tbl$.data('url-delete'),
                    method: 'POST',
                    params: { 'id[]': id_selecteds },
                });
                if (!result.confirmed || !result.data) return;

                if (result.data.status_code !== 1) {
                    ToastHelper.showError();
                    return;
                }

                ToastHelper.showSuccess();
                tbl$.DataTable().ajax.reload();
            });
        },
    });
    DataTableLoader.init_filter_is_status(tbl$);
});