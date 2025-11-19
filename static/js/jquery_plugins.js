$.fn.extend({
    deepNestObject(flatObject) {
        /**
         * Chuyển đổi một đối tượng phẳng thành đối tượng lồng nhau đệ quy
         * dựa trên dấu phân tách "__".
         *
         * Ví dụ: {"a__e__f": 5} -> {"a": {"e": {"f": 5}}}
         *
         * @param {object} flatObject Đối tượng đầu vào.
         * @returns {object} Đối tượng lồng nhau.
         */
        const result = {};
        const separator = '__';

        for (const [key, value] of Object.entries(flatObject)) {
            // Tách khóa thành các phần
            const parts = key.split(separator);

            // Sử dụng reduce để di chuyển qua các cấp độ lồng nhau
            parts.reduce((acc, part, index) => {
                // Nếu là phần tử cuối cùng, gán giá trị
                if (index === parts.length - 1) {
                    acc[part] = value;
                }
                // Nếu chưa phải phần tử cuối cùng, đảm bảo cấp độ hiện tại là một đối tượng
                else {
                    if (!acc[part] || typeof acc[part] !== 'object' || Array.isArray(acc[part])) {
                        acc[part] = {};
                    }
                    // Trả về đối tượng cấp độ tiếp theo để reduce tiếp tục
                    return acc[part];
                }
                return acc; // Chỉ trả về acc khi không phải phần tử cuối cùng (để reduce tiếp tục)
            }, result);
        }
        return result;
    },
    safeHtml(html_str){
        if (!html_str) return '';
        return DOMPurify.sanitize(html_str);
    },
    escapeHtml(str) {
        if (!str) return '';

        // return $('<div>').text(str).html();

        let data = Array.isArray(str) ? str.join(",") : str;
        if (typeof data !== "string") return data;
        return data
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },
})