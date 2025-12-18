$(document).ready(function () {
    const tbl$ = $('#datatables-product_variants');
    const dtb$ = DataTableLoader.init(tbl$, {
        ajax: {
            url: tbl$.data('url'),
            ...DataTableLoader.ajax_base(),
        },
        ordering: true,
        orderCellsTop: true,
        order: [[0, 'asc']],
        columns: [
            {
                data:'product.name',
                name: 'product',
                orderable: true,
                render(data, type, row) {
                    return data || '-';
                }
            },
            { 
                data: 'name',
                name: 'name',
                orderable: false,
                allowHtml: true,
                render(data, type, row) {
                    const url = tbl$.data('url-detail').replaceAll('__pk__', row['id'] || '');
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
                    return data || '-';
                }
            },
            DataTableLoader.col_is_price(),  
            DataTableLoader.col_is_active({ useToggle: true }),
        ],
        rowGroup: {
            dataSrc: 'product.name',
            startRender: function(rows, group) {
                return $('<tr/>')
                    .append('<td colspan="6" class="fw-bold bg-muted">'
                        + group + ' (' + rows.data().length + ' variants)</td>');
            }
        },
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

                const res = await SweetAlertHelper.confirmDelete({
                    url: tbl$.data('url-delete'),
                    method: 'POST',
                    params: { 'id[]': id_selecteds },
                });
                if(res){
                    if (res.cancelled){
                        console.log("User cancelled");
                    }
                    else if(res.status_code !==1){
                        ToastHelper.showError();
                    }
                    else{
                        ToastHelper.showSuccess();
                        tbl$.DataTable().ajax.reload();
                    }
                }else{
                    ToastHelper.showError();
                }
            });
        },
    });
    DataTableLoader.init_filter_is_status(tbl$)
    const filterProduct$ = tbl$.find('.dt-filter-row .dtb_filter_product');
    if(filterProduct$.length >0){
        Select2Helper.init(
            filterProduct$,
            {
                url:filterProduct$.data('url')
            }
        )
        filterProduct$.on('change', function () {
            tbl$.DataTable().column(filterProduct$).search($(this).val() || null).draw();
        });
    }
});