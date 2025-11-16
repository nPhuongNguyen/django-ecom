class DataTableLoader {
    static dt_container$(tbl$) {
        return tbl$.closest('.dt-container');
    }

    static dt_top$(tbl$) {
        return tbl$.closest('.dt-container').find('.dt-top');
    }
    

    static dt_select_container$(tbl$) {
        return tbl$.closest('.dt-container').find('.dt-select-container');
    }

    static dt_select_info$(tbl$) {
        return tbl$.closest('.dt-container').find('.dt-select-info');
    }
    static get_selected_row_data(table$) {
        let dtb = table$.DataTable();
        return dtb.rows({ selected: true }).data().toArray();
    }

    // --- AJAX CONFIG ---
    static ajax_dataSrc(json) {
        json.recordsTotal = json.count;
        json.recordsFiltered = json.count;
        return json.results;
    }

    static ajax_data(d) {
        const params = {
            page: (Math.floor(d.start / d.length) + 1) || 1,
            pageSize: d.length,
        };

        if (d?.search?.value) params.search = d.search.value;

        const order = (d.order || [])
            .map(o => {
                const name = d.columns[o.column]?.name;
                return name ? (o.dir === 'asc' ? name : '-' + name) : null;
            })
            .filter(Boolean);
        if (order.length) params.ordering = order.join(',');

        (d.columns || []).forEach(col => {
            if (col.searchable && col.name && col.search.value)
                params[col.name] = col.search.value;
        });

        return params;
    }

    static ajax_base() {
        return {
            data: DataTableLoader.ajax_data,
            dataSrc: DataTableLoader.ajax_dataSrc,
        };
    }

    // --- DOM / LAYOUT ---
    static dom() {
        return `
            <"dt-top flex flex-wrap items-center justify-between gap-2 mb-2"f>
            t
            <"dt-footer flex flex-wrap items-center justify-between gap-2 mt-2"
                <"l-portion"l>
                <"p-portion flex items-center gap-3"<"info-container"i>p>
            >
        `;
    }
    static language() {
        return {
            processing: "Đang xử lý...",
            loadingRecords: "Đang tải...",
            search: "",
            searchPlaceholder: "Tìm kiếm...",
            lengthMenu: "Hiển thị _MENU_ bản ghi",
            info: "Hiển thị _START_ - _END_ của _TOTAL_ bản ghi",
            infoEmpty: "Hiển thị 0 - 0 của 0 bản ghi",
            infoFiltered: "(lọc từ _MAX_ bản ghi)",
            zeroRecords: "Không tìm thấy bản ghi phù hợp",
            emptyTable: "Không có dữ liệu",
            paginate: {
                first: "«",
                previous: "‹",
                next: "›",
                last: "»"
            },
        };
    }

    static lengthMenu() { return [10, 25, 50, 100, 200]; }
    static pageLength() { return 10; }

    // --- RENDER SAFE TEXT ---
    static columns_render_text(columns) {
        return columns.map(item => ({
            ...item,
            render(data, type, row, meta) {
                const original = item.render || ((v) => v);
                const val = original(data, type, row, meta);
                
                if (type !== 'display') return val;

                // Nếu item.allowHtml === true → render HTML, không escape
                if (item.allowHtml) return val ?? '';

                // Ngược lại escape text bình thường
                const div = document.createElement('div');
                div.textContent = val ?? '';
                return div.innerHTML;
            }
        }));
    }

    // --- SELECT ROW ---
    static get_select_row(selectrow){
        if (selectrow === 'single') return { style: 'single', info: false };
        if (selectrow === 'multi') return { style: 'multi', info: false };
        return null;
    }

    static _init_select_row(settings, json, options, table$, dtb) {
        const selectRow = options?.['selectRow'] || null;
        const dt_search$ = DataTableLoader.dt_container$(table$).find('.dt-search');
        if (selectRow && dt_search$.length > 0) {
            dtb.on('draw select deselect', function () {
                const selectInfo$ = DataTableLoader.dt_select_info$(table$);
                const selectedRow = DataTableLoader.get_selected_row_data(table$);
                if (selectedRow.length > 0) {
                    selectInfo$.show();
                    selectInfo$.find('.dt-select-info-text').text(`${selectedRow.length} row selected`);
                } else {
                    selectInfo$.find('.dt-select-info-text').text('');
                    selectInfo$.hide();
                }
            });
            const select_info$ = $(`
                <div class="dt-select-info hidden items-center gap-2 text-primary text-sm font-medium">
                    <span class="dt-select-info-text"></span>
                </div>
            `);
            select_info$.insertAfter(dt_search$);
            const func_select_render = options?.['selectRowRender'] || null;
            if (func_select_render && typeof func_select_render === 'function') {
                func_select_render(select_info$);
            }
            const addUrl = table$.data('url-add');
            if (addUrl) {
                const addBtn$ = $('<button class="kt-btn kt-btn-primary ml-2">Thêm mới</button>');
                DataTableLoader.dt_top$(table$).append(addBtn$);
                addBtn$.on('click', () => {
                    window.location.href = addUrl;
                });
            }
        }
    }

    static initAddButton(table$, label = 'Thêm mới', onClick) {
        const dt_top$ = DataTableLoader.dt_top$(table$);
        if (!dt_top$ || dt_top$.length === 0) return;

        const addBtn$ = $(`<button class="kt-btn kt-btn-primary ml-2">${label}</button>`);
        dt_top$.append(addBtn$); 
        if (typeof onClick === 'function') addBtn$.on('click', onClick);
    }

    static baseInitComplete(settings, json, options, table$){
        const dtb = table$.DataTable();
        const dt_search$ = DataTableLoader.dt_container$(table$).find('.dt-search');
        dt_search$.addClass('min-w-64 max-w-96')
        dt_search$.find('input').addClass('kt-input w-full');
        DataTableLoader._init_select_row(settings, json, options, table$, dtb);
    }

    // --- INIT ---
    static init(table$, options) {
        options.select = DataTableLoader.get_select_row(options.selectRow || 'single');
        options.columns = DataTableLoader.columns_render_text(options.columns || []);

        return table$.DataTable({
            dom: options.dom || DataTableLoader.dom(),
            language: options.language || DataTableLoader.language(),
            lengthMenu: options.lengthMenu || DataTableLoader.lengthMenu(),
            pageLength: options.pageLength || DataTableLoader.pageLength(),
            searchDelay: 500,
            serverSide: true,
            processing: true,
            responsive: true,
            ...options,
            initComplete: function (settings, json) {
                DataTableLoader.baseInitComplete(settings, json, options, table$);
            },
        });
        
    }
    static render_price(data, type, row, meta) {
        if (type !== 'display') return data; 
        if (data == null) return '-';
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(data);
    }

    static column_price(name = 'price', orderable = false) {
        return {
            data: name,
            name: name,
            orderable: orderable,
            render: DataTableLoader.render_price
        };
    }
}
