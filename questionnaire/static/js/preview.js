$(function(){
    disableInputFields(true);
    $('#edit_questionnaire_link').on('click', function(){
        disableInputFields(false);
    });
});

function disableInputFields(status) {
    $('.form-content :input').each(function () {
        $(this).prop('disabled', status);
    });
    $('.add-more').prop('disabled', status);
}
