class FilePondHelper {
    static registerPlugins() {
        FilePond.registerPlugin(
            FilePondPluginImagePreview
        );
    }
    static init(selector) {
        const input = document.querySelector(selector);
        if (!input) return null;

        const pond = FilePond.create(input, {
            allowMultiple: false,
            allowImagePreview: true,
            labelIdle: 'Kéo thả ảnh vào đây hoặc <span class="filepond--label-action">Chọn ảnh</span>',
            credits: false
        });

        return pond;
    }
}
