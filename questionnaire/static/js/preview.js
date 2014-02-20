
$(document).ready(function() {
    $('.add-more').attr('disabled','disabled');
    var edit = '<span class="green bold"><i class="glyphicon glyphicon-floppy-disk"></i>EDIT</span>'
    $('#save_draft_button').html(edit);
    $('#preview_modal_btn').html(edit);

    $("body").show();
    $('textarea').autosize().trigger('autosize.resize');
});