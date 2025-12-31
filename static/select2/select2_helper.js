class Select2Helper {
    static buildAjaxConfig(url, extraData, valueField, textField) {
        return {
            url,
            dataType: 'json',
            delay: 250,
            headers: {
                'Token': AuthStorage.getToken(),
            },
            data:  (params) => 
                Select2Helper.buildData(params, extraData),
            processResults: (response) =>
                Select2Helper.mapResults(response, valueField, textField)
        };
    }

    static buildData(params, extraData) {
        return {
            search: params.term || '',
            page: params.page || 1,
            page_size: params.page_size || 10,
            ...extraData
        };
    }

    static mapResults(response, valueField, textField) {
        // check status_code
        if (!response || response.status_code !== 1) {
            return { results: [] };
        }

        const results = response.data?.result || [];
        const more = response.data?.next_page > (response.data?.previous_page || 0);

        return {
            results: results.map(item => ({
                id: item[valueField],
                text: item[textField],
                rawItem: item
            })),
            pagination: { more }
        };
    }
    static init(selector, config) {
        const $el = $(selector);
        if (!$el.length) return null;

        const {
            url = null,
            data = null,
            valueField = 'id',
            textField = 'name',
            extraData = {},
            placeholder = "Chọn...",
            multiple = false
        } = config;

        const baseConfig = {
            placeholder,
            allowClear: true,
            minimumInputLength: 0,
            theme: 'tailwindcss-3',
            width: '100%',
            multiple 
        };

        // ===== 1. STATIC DATA =====
        if (Array.isArray(data)) {
            return $el.select2({
                ...baseConfig,
                data: data.map(item => ({
                    id: item[valueField],
                    text: item[textField],
                    rawItem: item
                }))
            });
        }

        // ===== 2. AJAX =====
        if (url) {
            const ajaxConfig = Select2Helper.buildAjaxConfig(
                url,
                extraData,
                valueField,
                textField
            );

            return $el.select2({
                ...baseConfig,
                ajax: ajaxConfig
            });
        }

        return null;
    }

}
