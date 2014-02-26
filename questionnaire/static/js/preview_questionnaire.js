$(function(){
    $('#preview_modal').on('show.bs.modal', function(){
        console.log('haha')
        var questionnaire_preview_url = "/questionnaire/preview/";
        $.get(questionnaire_preview_url, function( data ) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#preview-content").html()
            $( "#ajax-content" ).html(content);
            disable_modal_input_fields();
        });
    });
    disable_modal_input_fields();

    $('#edit_questionnaire_link').on('click', function(){
        disableInputFields();
    });
});

function disable_modal_input_fields(){
    $('.tab-content :input').each(function() {
       $(this).attr('disabled','disabled');
    });
};

function disableInputFields(status) {
    $('.form-content :input').each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
}