$(function(){
    $('#preview_modal').on('show.bs.modal', function(){
        console.log('haha')
        var questionnaire_preview_url = "/questionnaire/preview/";
        $.get(questionnaire_preview_url, function( data ) {
            var $holder = $('<div></div>').append(String(data));
            var content =  $holder.find("#preview-content").html()
            $( "#ajax-content" ).html(content);
            disable_fields();
        });
    });
    disable_fields();
});

function disable_fields(){
    $('.tab-content :input').each(function() {
       $(this).attr('disabled','disabled');
    });
};