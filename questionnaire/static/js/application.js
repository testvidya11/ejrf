$(document).ready(function() {

    $('a[data-toggle=popover]').popover();
    $('a[data-toggle=popover]').popover('destroy');
    $(this).next('.question-group').remove();
    $(this).prev('.multiple-hr').remove();
    $(this).remove();

    $('a[data-toggle=popover]').popover();
    load_organization_template();

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
    $(selector).after('<button type="button" id="delete_more" class="btn btn-default red delete-more close">×</button>');
    $(selector).after("<hr class='multiple-hr'/>");

    $('a[data-toggle=popover]').popover();

}

$('#add_more').on('click', function(event) {
    cloneMore($(this).prev('.question-group'), 'service');
});

function load_organization_template(){
    $('.radio-roles').on('change', function(){
     var template = $("#organization-template").html();
        $(this).parents('ul').after(template);
        $('#id_organization').remove();
    })
}