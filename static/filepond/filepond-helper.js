class FilePondHelper {
    static registerPlugins() {
        FilePond.registerPlugin(
            FilePondPluginImagePreview
        );
    }
    static init(selector, onFileGet) {
        const input = document.querySelector(selector);
        if (!input) return null;

        const pond = FilePond.create(input, {
            allowMultiple: false,
            allowImagePreview: true,
            labelIdle: 'Kéo thả ảnh vào đây hoặc <span class="filepond--label-action">Chọn ảnh</span>',
            credits: false,
            onaddfile: (err, fileItem) => {
                if (!err) {
                    const file = fileItem.file;
                    onFileGet(file);
                }
            }
        });

        return pond;
    }
}
