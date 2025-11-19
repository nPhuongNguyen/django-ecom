$(document).ready(function () {
   const frm$ = $('#frm_create_product')
   FilePondHelper.registerPlugins();

   const img_url = $('input[name="image"]').val();
   const img_check$ = $('#image_check');
   const hidden$ = frm$.find('input[name="image"]');
   
   let pond;
   
   pond = FilePondHelper.init("#inp_image", img_url, (pondInstance) => { 
      pond = pondInstance; 
      
      pond.on('addfile', () => {
         if(pond._skipNextAddFile){
            pond._skipNextAddFile = false
            return;
         }
         hidden$.val('has-file'); 
         hidden$.valid();   
         img_check$.val("1"); 
         console.log("img_check",img_check$.val());
      });
      
      pond.on('removefile', () => {
         hidden$.val('');
         hidden$.valid();
         img_check$.val("1");
         console.log("img_check",img_check$.val());
      });
   });

   const validator = FormValidateLoader.init(
      frm$,
      {
         submitHandler: async function (form, event) {
               event.preventDefault();
               const data = new FormData(frm$[0]);
               data.delete('filepond');
               data.delete('image');
               
               if (pond && pond.getFiles().length > 0) {
                  const file = pond.getFiles()[0].file;
                  data.append('image', file);
               } else {
                  data.delete('image');
               }
               
               const result = await SweetAlertHelper.confirmSave({ 
                  url: frm$.data('url'), 
                  method : 'PUT',
                  data: data 
               });
               
               if (result && result.status === 'error') {
                  console.log(result.data);
                  if (typeof result.data === 'object') {
                     validator.showErrors(result.data)
                  }
                  return;
               }
               else if (result && result.status == 'success'){
                  FormValidateLoader.savedNext(event, {
                     url_save: frm$.data('url-list'),
                     url_add_another: frm$.data('url-add'),
                     url_continue_editing: frm$.data('url-detail').replaceAll('__slug__', result.data.results.slug)
                  });
                  return;
               }
         }
      }
    );
});