$(function(){
    $('#new-section-modal-form').validate({
        rules: { 'name': 'required', 'title': 'required'}
    });
    $('#new-subsection-modal-form').validate({
        rules: { 'title': 'required'}
    });
});