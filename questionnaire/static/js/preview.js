
$(document).ready(function() {
    $('.add-more').attr('disabled','disabled');
    $('#cancel_button').hide();
    $('#save_draft_button').hide();

    $(this).find('.form-content :input').each(function() {
       $(this).attr('disabled','disabled');
    });

    $("body").show();
    $('textarea').autosize().trigger('autosize.resize');
});