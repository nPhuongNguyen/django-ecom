$(document).ready(function () {
    const selectProduct$ = $('#inp_select_product');
    const apiURL$ = selectProduct$.data('url');
    Select2Helper.init(selectProduct$, {
        url: apiURL$,            
        valueField: 'id',       
        textField: 'name'   
    });
})