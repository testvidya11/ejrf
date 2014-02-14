$(function(){
    $('#create-section-modal').validate({
        rules: {
            'name': 'required',
            'title': 'required'
        },
        messages:{
            'name': 'This field is required',
            'title': 'This field is required'
        }
    })
})