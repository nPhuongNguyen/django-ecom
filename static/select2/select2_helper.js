class Select2Helper {
    static init(selector, config) {
        const $el = $(selector);
        if (!$el.length) return null;

        const {
            url,
            valueField = 'id',
            textField = 'name',
            extraData = {},
            templateResult,
            templateSelection
        } = config;

        const instance = $el.select2({
            placeholder: "Chọn...",
            allowClear: true,
            width: '100%',
            minimumInputLength: 0,
            ajax: {
                url,
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return {
                        search: params.term || '',
                        page: params.page || 1,
                        pageSize: params.page_size || 10,                  
                        ...extraData           
                    };
                },
                processResults: (data) => {
                    return {
                        results: (data.results || []).map(item => ({
                            id: item[valueField],
                            text: item[textField],
                            rawItem: item
                        })),
                        pagination: {
                            more: !!data.next 
                        }
                    };
                },
                cache: true
            },
            templateResult: item => {
                if (!item.id) return item.text;
                if (typeof templateResult === 'function') return templateResult(item);
                const currentValue = $el.val();
                const isSelected = currentValue == item.id;
                return $(`
                    <div class="flex justify-between items-center">
                        <span>${item.text}</span>
                        ${
                            isSelected
                                ? `<span>
                                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                                            <path d="M12 2C6.49 2 2 6.49 2 12C2 17.51 6.49 22 12 22C17.51 22 22 17.51 22 12C22 6.49 17.51 2 12 2ZM16.78 9.7L11.11 15.37C10.97 15.51 10.78 15.59 10.58 15.59C10.38 15.59 10.19 15.51 10.05 15.37L7.22 12.54C6.93 12.25 6.93 11.77 7.22 11.48C7.51 11.19 7.99 11.19 8.28 11.48L10.58 13.78L15.72 8.64C16.01 8.35 16.49 8.35 16.78 8.64C17.07 8.93 17.07 9.4 16.78 9.7Z" fill="#4564ED"/>
                                        </svg>
                                    </span>`
                                : ''
                        }
                    </div>
                `);
            },
            templateSelection: item => {
                if (!item.id) return item.text;
                if (typeof templateSelection === 'function') return templateSelection(item);
                return item.text;
            }
        });
        const $container = $el.data('select2')?.$container;
        if ($container) {
            $container.css('min-width', '200px');
            $container.find('.select2-selection__rendered').css('white-space', 'normal');
        }
        $el.on('select2:open', () => {
            const $search = $('.select2-search__field');
            $search.addClass('kt-input'); 
            $search.attr('placeholder', 'Tìm kiếm...');
        });

        return instance;
    }
}

