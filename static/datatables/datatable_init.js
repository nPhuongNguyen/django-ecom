class DataTableLoader {

    static dt_search$(tbl$) {
        return tbl$.closest('.dt-container').find('.dt-search');
    }
    static dt_select_info$(tbl$) {
        return tbl$.closest('.dt-container').find('.dt-select-info');
    }
    static get_selected_row_data(table$) {
        let dtb = table$.DataTable();
        return dtb.rows({ selected: true }).data().toArray();
    }

    static dt_add$(tbl$){
        return tbl$.closest('.dt-container').find('.dt-add');
    }

    // --- AJAX CONFIG ---
    static ajax_dataSrc(json) {
        json.recordsTotal = json.data.count;
        json.recordsFiltered = json.data.count;
        return json.data.result;
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
            <"dt-header flex items-center justify-between py-3 px-4"
                <"flex items-center gap-3"
                    <"dt-search"f>
                    <"dt-select-info">
                >
                <"dt-add ms-auto"> 
            >
            <t>
            <"dt-footer flex justify-between items-center"
                <"kt-datatable-length" l>
                <"flex items-center gap-3"
                    <"kt-datatable-info" i>
                    <"kt-datatable-pagination" p>
                >
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

    // --- SELECT ROW ---
    static get_select_row(selectrow){
        if (selectrow === 'single') return { style: 'single', info: false };
        if (selectrow === 'multi') return { style: 'multi', info: false };
        return null;
    }
    static info_selected_row(table$, options, select_info, selectedRows) {
        const count = selectedRows.length;
        if (count === 0) {
            return select_info.empty().hide();
        }

        // Hiển thị nội dung khi có hàng được chọn
        const htmlContent = `
            <div class="dt-select-info-rows flex gap-3 rounded-lg">
    
                <div class="flex items-center gap-2">
                    <i class="ki-filled ki-information-2 text-primary text-xl"></i>
                    <span class="font-semibold text-gray-700">
                        Đã chọn: <span class="text-primary">${count}</span> hàng
                    </span>
                </div>

                <div class="info-actions-container flex items-center">
                    
                </div>
                
            </div>
        `;
        select_info.html(htmlContent).show();
        if (options && typeof options.selectRowRender === 'function') {
            const dt_select_rows$ = select_info.find('.dt-select-info-rows');
            const actionContainer = dt_select_rows$.find('.info-actions-container');
            options.selectRowRender(actionContainer, selectedRows, table$);
        } 
    }


    static _init_select_row(settings, json, options, table$, dtb) {
        const dt_search$ = DataTableLoader.dt_search$(table$);
        if (dt_search$.length > 0) {
            const searchInput$ = dt_search$.find('input[type="search"]');
            if (searchInput$.length > 0) {
                searchInput$.addClass('kt-input w-48');
            }
        }
        /* 
            draw để bắt sự kiện load lại datatable
            select deselect để bắt sự kiện chọn hàng
        */
        const dt_select_info$ = DataTableLoader.dt_select_info$(table$);
        dtb.on('draw select deselect', function () {
            const selectedRowData$ = DataTableLoader.get_selected_row_data(table$);
            DataTableLoader.info_selected_row(table$, options, dt_select_info$, selectedRowData$);
        });
       
    }
    static init_filter_is_status(table$) {
        const filter$ = table$.find('thead select.dtb_filter_status');
        if(filter$.length > 0){
            Select2Helper.init(filter$, {
                data:[
                    {
                        'id':true,
                        'name':'Active'
                    },
                    {
                        'id':false,
                        'name':"Deactive"
                    }
                ]         
            });
            filter$.on('change', function () {
                table$.DataTable().column(filter$).search($(this).val() || null).draw();
            });
        }
        
    }

    static initAddButton(table$, label = 'Thêm mới') {
        const dt_add$ = DataTableLoader.dt_add$(table$);
        if (!dt_add$ || dt_add$.length === 0) return;

        const addBtn$ = $(`<button class="kt-btn kt-btn-primary">${label}</button>`);
        dt_add$.append(addBtn$); 
    }

    static baseInitComplete(settings, json, options, table$){
        const dtb = table$.DataTable();
        DataTableLoader._init_select_row(settings, json, options, table$, dtb);
        DataTableLoader.initAddButton(table$);
    }

    // --- INIT ---
    static init(table$, options) {
        const selectRowOption = DataTableLoader.get_select_row(options.selectRow || 'single');
        if (selectRowOption) {
            selectRowOption.selector = 'td:not(:has(a)):not(:has(.toggle-active))';
        }
        options.select = selectRowOption;

        const dt = table$.DataTable({
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
        const checkOnToggle = options.ontoggleActive;
        if (checkOnToggle && typeof checkOnToggle === "function"){
            const dtb$ = table$.DataTable();
            dtb$.on("change", ".toggle-active", function () {
                const id = $(this).data("id");
                checkOnToggle(id);
            });
        }
        return dt; 
    }

    static formatPriceOnInput(value) {
        if (!value) return "";
        value = value.toString().replace(".", ",");
        let parts = value.split(",");
        parts[0] = Number(parts[0]).toLocaleString("vi-VN");
        return parts.join(",");
    }
    static col_is_price(opts) {
        const {
            visible,
            orderable,
            ...restProps
        } = {
            visible: true,
            orderable: false,
            ...opts,
        }
        return {
            ...restProps,
            data: 'price',
            name: 'price',
            orderable: !!orderable,
            visible: !!visible,
            render:  function(data, type, row) {
                return DataTableLoader.formatPriceOnInput(data) || '-';
            }
        };
    }

    static col_is_status(opts) {
        const {
            visible,
            orderable,
            useToggle,
            ...restProps
        } = {
            visible: true,
            orderable: false,
            useToggle: false,
            onToggle: null,
            ...opts,
        };

        return {
            ...restProps,
            data: 'is_active',
            name: 'is_active',
            orderable: !!orderable,
            visible: !!visible,
            render: (data, type, row, meta) => {
                const disabledAttr = useToggle ? "" : "disabled";
                return `
                    <input type="checkbox"
                        class="kt-switch toggle-active"
                        data-id="${row.id}"
                        ${data ? "checked" : ""}
                        ${disabledAttr}
                    />
                `;
            }
        };
    }

}
