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
            DataTableLoader.col_is_active(),
            DataTableLoader.col_is_price(),  
        ],
        selectRow: 'multi',
        selectRowRender: (select_info$) => {
            const btnDestroy$ = $(`<button class="kt-btn kt-btn-destructive">Delete selected</button>`);
            select_info$.append(btnDestroy$);
            btnDestroy$.on('click', async function (){
                const id_selecteds = DataTableLoader.get_selected_row_data(tbl$).map(row => row.id);
                if (id_selecteds.length === 0) return;
                const result = await SweetAlertHelper.confirmDelete({
                    url: tbl$.data('url-delete') + '?' + $.param({'ids': id_selecteds}),
                    table: tbl$,
                })
                if (result && result.status === 'error') {
                    console.log(result.data);
                    if (typeof result.data === 'object') {
                        validator.showErrors(result.data)
                    }
                    return;
                }
                else if (result && result.status == 'success'){
                    tbl$.DataTable().ajax.reload(null, false);
                    return;
                }
            })
        },
        
    });
    
});