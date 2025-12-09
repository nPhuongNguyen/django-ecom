$(document).ready(async function () {
    const selectCategory$ = $('#inp_select_category');
    const apiURL$ = selectCategory$.data('url');
    Select2Helper.init(selectCategory$, {
        url: apiURL$,            
        valueField: 'id',       
        textField: 'name'   
    });
})