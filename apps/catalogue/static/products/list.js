$(document).ready(function () {
    const tbl$ = $('#datatables-products');
    const dtb = DataTableLoader.init(tbl$, {
        ajax: {
            url: tbl$.data('url-list'),
            ...DataTableLoader.ajax_base(),
        },
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
            DataTableLoader.col_is_active({ useToggle: true }),
        ],
        ontoggleActive: async (id)=>{
            const result = await SweetAlertHelper.confirmSave({
                url: tbl$.data('url-change-status').replaceAll('__pk__', id),
                method: 'POST',
            });
            try{
                if (result.cancelled){
                    console.log("User cancelled");
                }
                else if (result.errors){
                    ToastHelper.error();
                }
                else{
                    ToastHelper.success();
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

                const res = await SweetAlertHelper.confirmDelete({
                    url: tbl$.data('url-delete'),
                    method: 'POST',
                    params: { 'id[]': id_selecteds },
                });
                if (res.cancelled){
                    console.log("User cancelled");
                }else if(res.errors){
                    ToastHelper.error();
                }else{
                    ToastHelper.success();
                    tbl$.DataTable().ajax.reload();
                }
            });
        },
    });
    
});