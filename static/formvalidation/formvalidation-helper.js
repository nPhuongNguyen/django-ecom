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
                remote: "Hãy sửa cho đúng.",
                email: "Hãy nhập email.",
                url: "Hãy nhập URL.",
                date: "Hãy nhập ngày.",
                dateISO: "Hãy nhập ngày (ISO).",
                number: "Hãy nhập số.",
                digits: "Hãy nhập chữ số.",
                creditcard: "Hãy nhập số thẻ tín dụng.",
                equalTo: "Hãy nhập thêm lần nữa.",
                extension: "Phần mở rộng không đúng.",
                maxlength: $.validator.format("Hãy nhập từ {0} kí tự trở xuống."),
                minlength: $.validator.format("Hãy nhập từ {0} kí tự trở lên."),
                rangelength: $.validator.format("Hãy nhập từ {0} đến {1} kí tự."),
                range: $.validator.format("Hãy nhập từ {0} đến {1}."),
                max: $.validator.format("Hãy nhập từ {0} trở xuống."),
                min: $.validator.format("Hãy nhập từ {0} trở lên.")
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

    static savedNext(event_of_submit_handler, opts, timeout = 200) {
        if ($.fn.getParam('is_popup') === '1') {
            setTimeout(
                () => window.close(),
                200
            )
        }

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
            const dataNext = ele$.data('next');
            if (dataNext === null || dataNext === 'add') {
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