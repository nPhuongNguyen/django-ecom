class UppyUploader {
    static addExistingFile(uppyInstance, url) {
        if (!url) return;

        fetch(url)
            .then(res => res.blob())
            .then(blob => {
                const fileName = url.split('/').pop() || 'file.png';
                const file = new File([blob], fileName, { type: blob.type || 'image/png' });
                uppyInstance.addFile({
                    id: 'existing-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
                    name: file.name,
                    type: file.type,
                    data: file,
                    preview: URL.createObjectURL(file),
                    meta: { isRemote: true }
                });
            })
            .catch(error => {
                console.error('Error adding existing file:', error);
                uppyInstance.info('Lỗi khi tải ảnh: ' + url, 'error');
                const fileName = url.split('/').pop() || 'file.png';
                uppyInstance.addFile({
                    id: 'existing-error-' + Date.now() + '-' + Math.floor(Math.random() * 1000),
                    name: fileName,
                    type: 'image/png',
                    data: new Blob(),
                    // preview: '/static/images/image-error.png', 
                    meta: { isRemote: true, error: true }
                });
            });
    }


    static init(targetSelector, url, opts = {}) {
        this.injectCustomCSS();
        if (!targetSelector) return null;

        const dropPasteFilesText = gettext('Drop files here or %{browseFiles}');

        const allowExtensions = opts.uppyOptions?.restrictions?.allowedFileTypes || ['.jpg', '.jpeg', '.png'];
        const maxNumberOfFiles = opts.uppyOptions?.restrictions?.maxNumberOfFiles || 1;
        const acceptedFileTypesText = gettext('Accepted file types: ') + allowExtensions.join(', ');

        const maxFileSize=opts.uppyOptions?.restrictions?.maxFileSize || 1000 * 1024;
        const maxFileSizeText = gettext('Max file size: ') + (maxFileSize / 1024) + 'KB';

        const uppy = new Uppy.Uppy({
            restrictions: {
                allowedFileTypes: allowExtensions,
                maxNumberOfFiles: maxNumberOfFiles,
                maxFileSize: maxFileSize,
            },
            autoProceed: true,
            locale: {
                strings: {
                    dropPasteFiles: dropPasteFilesText + "\n" + acceptedFileTypesText + "\n" + maxFileSizeText,
                    browseFiles: gettext('browse files'),
                    xFilesSelected: gettext('%{smart_count} file selected'),
                    uploadingXFiles: gettext('Uploading %{smart_count} file'),
                    exceedsSize: gettext('%{file} exceeds maximum allowed size of %{size}'),
                    youCanOnlyUploadFileTypes: gettext('You can only upload: %{types}'),
                },
            },
            ...opts.uppyOptions,
        });
        

        uppy.use(Uppy.Dashboard, {
            inline: true,
            target: targetSelector,
            width: '100%',
            height: 400,
            proudlyDisplayPoweredByUppy: false,
            hideCancelButton: true,
            hideUploadButton: true,
            note: gettext(`Only JPG, JPEG, PNG files are allowed. Max file size: ${(maxFileSize / 1024)}KB.`),
            ...opts.dashboardOptions,
        });

        uppy.on('file-added', file => {
            if (!uppy._initialFiles) {
                uppy._initialFiles = [];
            }
            if (file.meta.isRemote) {
                uppy._initialFiles.push(file);
            }
        });


        if (url) {
            const urlList = url.split(';');
            urlList.forEach(u => this.addExistingFile(uppy, u));
        }

        return uppy;
    }

    static injectCustomCSS() {
        const style = document.createElement('style');
        style.textContent = `
        .uppy-Dashboard-AddFiles-title {
            white-space: pre-line !important;
        }
    `;
        document.head.appendChild(style);
    }

    static getFiles(uppyInstance) {
        if (!uppyInstance) return [];
        return uppyInstance.getFiles();
    }

    static hasChanged(uppyInstance) {
        if (!uppyInstance) return false;

        const current = uppyInstance.getFiles();
        const initial = uppyInstance._initialFiles || [];

        // 1. Có file mới (không phải remote)?
        const hasNew = current.some(f => !f.meta.isRemote);

        // 2. Có file remote bị xóa?
        const initialIds = initial.map(f => f.id);
        const currentIds = current.map(f => f.id);
        const hasDeleted = initialIds.some(id => !currentIds.includes(id));

        return hasNew || hasDeleted;
    }


}
