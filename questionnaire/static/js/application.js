$(document).ready(function() {

    $('a[data-toggle=popover]').popover();

});


$('#add_more').click(function(event) {
    cloneMore($(this).prev('.question-group'), 'service');
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
    $(selector).after("<hr class='multiple-hr'/>");
    $('a[data-toggle=popover]').popover();

}