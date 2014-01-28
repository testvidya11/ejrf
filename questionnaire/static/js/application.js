$(document).ready(function() {

    $('a[data-toggle=popover]').popover();

});


function cloneMore(selector, type) {
    $('a[data-toggle=popover]').popover('destroy');

    var newElement = $(selector).clone(true);
    newElement.find(':input').each(function() {
        // Reset cloned inputs
        $(this).val('');
        $(this).removeAttr('checked');
        $(this).removeAttr('selected');
    });

    $(selector).after(newElement);
    $(selector).after('<button type="button" class="btn btn-default red delete-more close">×</button>');
    $(selector).after("<hr class='multiple-hr'/>");

    $('a[data-toggle=popover]').popover();

}

$('#add_more').on('click', function(event) {
    cloneMore($(this).prev('.question-group'), 'service');
});

$(document).on('click', '.delete-more', function() {
    $('a[data-toggle=popover]').popover('destroy');

    $(this).next('.question-group').remove();
    $(this).prev('.multiple-hr').remove();
    $(this).remove();

    $('a[data-toggle=popover]').popover();
});