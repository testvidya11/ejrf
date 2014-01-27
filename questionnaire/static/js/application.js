$('a[data-toggle=popover]').popover();

$('body').on('click', function (e) {
    $('[data-toggle="popover"]').each(function () {
        //the 'is' for buttons that trigger popups
        //the 'has' for icons within a button that triggers a popup
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
            $(this).popover('hide');
        }
    });
});


$('#add_more').click(function() {
    cloneMore($(this).prev('.question-group'), 'service');
});

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    newElement.find(':input').each(function() {
        // Reset cloned inputs
        $(this).val('');
        $(this).removeAttr('checked');
        $(this).removeAttr('selected');
    });

    $(selector).after(newElement);
    $(selector).after("<hr class='multiple-hr'/>");
}