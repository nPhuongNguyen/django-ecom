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
                    return `<a class="kt-link kt-link-underline" href="${url}" onclick="event.stopPropagation();">${data || '-'}</a>`;
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
            DataTableLoader.column_price(),
        ],
        selectRow: 'multi',
        selectRowRender: (select_info$) => {
            const btnDestroy$ = $(`<button class="kt-btn kt-btn-destructive">Delete selected</button>`);
            select_info$.append(btnDestroy$);
            btnDestroy$.on('click', function (){
                const id_selecteds = DataTableLoader.get_selected_row_data(tbl$).map(row => row.id);
                if (id_selecteds.length === 0) return;
                SweetAlertHelper.confirmDelete({
                    url: tbl$.data('url-delete') + '?' + $.param({'ids': id_selecteds}),
                    table: tbl$,
                })
            })
        },
        
    });
    
});