class FilePondHelper {
    static registerPlugins() {
        FilePond.registerPlugin(
            FilePondPluginImagePreview
        );
    }
    static init(selector, defaultUrl = null, onReady = null) {
        const input = document.querySelector(selector);
        if (!input) return null;

        const options = {
            allowMultiple: false,
            allowImagePreview: true,
            labelIdle: 'Kéo thả ảnh vào đây hoặc <span class="filepond--label-action">Chọn ảnh</span>',
            credits: false
        };

        const pond = FilePond.create(input, options);
        pond._skipNextAddFile = !!defaultUrl; 
        
        if (defaultUrl && defaultUrl.trim() !== '') {
            fetch(defaultUrl)
                .then(res => {
                    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                    return res.blob();
                })
                .then(blob => {
                    const file = new File([blob], defaultUrl.split('/').pop(), { type: blob.type });
                    pond.addFile(file);
                })
                .catch(error => {
                    console.error('Error loading image from URL:', error);
                    console.log('URL tried:', defaultUrl);
                })
                .finally(() => {
                    if (onReady) onReady(pond);
                });
        } else {
            if (onReady) onReady(pond);
        }
        return pond;
    }
}