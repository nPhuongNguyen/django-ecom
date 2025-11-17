FilePondHelper.registerPlugins();
let selectedFile = null;

FilePondHelper.init("#inp_image", (file) => {
    selectedFile = file;
});
