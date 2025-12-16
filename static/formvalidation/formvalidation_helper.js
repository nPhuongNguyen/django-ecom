class FormValidateLoader {
    static formData(form, opts) {
        const {
            name_type_list,
            nest_key,
        } = {
            name_type_list: [],
            nest_key: false,
            ...opts,
        };

        const frm$ = $(form);
        let payload = {};

        function appendValue(key, value) {
            if (payload.hasOwnProperty(key)) {
                if (Array.isArray(payload[key])) {
                    payload[key].push(value);
                } else {
                    payload[key] = [payload[key], value];
                }
            } else {
                if (name_type_list.indexOf(key) !== -1) {
                    payload[key] = [value];
                } else {
                    payload[key] = value;
                }
            }
        }

        frm$.serializeArray().map(
            item => {
                const name = item['name'];
                const value = item['value'];
                if (name) {
                    let inp$ = frm$.find(`:input[name=${name}]`);
                    if (inp$.length === 0) {
                        inp$ = $('body').find(`:input[name=${name}][form=${frm$.attr('id')}]`);
                    }

                    if (inp$.length === 0) {
                        appendValue(name, value);
                    } else if (inp$.is("input[type='checkbox']")) {
                        appendValue(name, value === "on");
                    } else {
                        appendValue(name, value);
                    }
                }
            }
        )
        frm$.find("input[type=checkbox]").each(function () {
            const name = $(this).attr('name');
            payload[name] = $(this).is(':checked');
        });

        if (nest_key === true) payload = $.fn.deepNestObject(payload);
        return payload;
    }

    static disable_temp_submit(form, time_seconds = 1000) {
        const btn_submit$ = $(form).find('button[type=submit], button:not([type])').not(':disabled');
        if (btn_submit$.length > 0){
            btn_submit$.prop('disabled', true);
            setTimeout(
                () => btn_submit$.prop('disabled', false),
                time_seconds
            )
        }
    }

    static init(frm$, options) {
        return new FormValidateLoader(frm$).init(options);
    }

    constructor(frm$) {
        this.frm$ = frm$;
    }

    init(options) {
        if ($('html').attr('lang') === 'vi') {
            $.extend($.validator.messages, {
                required: "Trường dữ liệu này là bắt buộc.",
                remote: "Dữ liệu không hợp lệ.",
                email: "Email không hợp lệ.",
                url: "URL không hợp lệ.",
                date: "Ngày không hợp lệ.",
                dateISO: "Ngày không đúng định dạng ISO.",
                number: "Vui lòng nhập số hợp lệ.",
                digits: "Chỉ được nhập chữ số.",
                creditcard: "Số thẻ tín dụng không hợp lệ.",
                equalTo: "Giá trị nhập lại không khớp.",
                extension: "Phần mở rộng không hợp lệ.",
                maxlength: $.validator.format("Tối đa {0} ký tự."),
                minlength: $.validator.format("Tối thiểu {0} ký tự."),
                rangelength: $.validator.format("Từ {0} đến {1} ký tự."),
                range: $.validator.format("Giá trị từ {0} đến {1}."),
                max: $.validator.format("Giá trị ≤ {0}."),
                min: $.validator.format("Giá trị ≥ {0}.")
            });
        }

        const submitHandler = options?.['submitHandler'] || function (form, event) {
        };

        return this.frm$.validate({
            ...options,
            errorPlacement: function (error, element) {
                error.appendTo(element.parent());
            },

            submitHandler: (form, event) => {
                const btn_submit$ = $(form).find('button[type=submit], button:not([type])').not(':disabled');
                btn_submit$.prop('disabled', true);
                setTimeout(
                    () => btn_submit$.prop('disabled', false),
                )

                submitHandler.bind(this)(form, event);
            }
        });
    }

    static savedNext(event_of_submit_handler, opts, timeout = 1500) {
        const {
            url_save,
            url_add_another,
            url_continue_editing,
        } = {
            'url_save': '',
            'url_add_another': '',
            'url_continue_editing': '',
            ...opts,
        }

        const submitter = event_of_submit_handler.originalEvent.submitter;
        let funcNext = () => window.location.reload();
        if (submitter) {
            const ele$ = $(submitter);
            const dataNext = ele$.data('action');
            if (dataNext === null || dataNext === 'save') {
                funcNext = () => {
                    window.location.href = url_save;
                }
            }
            if (dataNext === 'add_another') {
                funcNext = () => {
                    window.location.href = url_add_another;
                }
            }
            if (dataNext === 'continue_editing') {
                funcNext = () => {
                    window.location.href = url_continue_editing;
                }
            }
        }
        setTimeout(funcNext, timeout);
    }
}