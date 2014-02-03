var form_has_changed = false;

$(document).ready(function() {

    $('a[data-toggle=popover]').popover();
    load_organization_template();

    warn_before_navigating_away();

});

function cloneMore(selector) {
    $('a[data-toggle=popover]').popover('destroy');

    var newElement = $(selector).clone(true);
    updateFormCounts(newElement);

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

function updateFormCounts(form_element){
    form_element.find(':input').each(function() {
        var inputType = $(this).attr('name').split('-', 1)[0];
        var total = $('#id_' + inputType + '-TOTAL_FORMS').val();

        var name = $(this).attr('name').replace(/[\d]+/g, total.toString());
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        total++;

        $('#id_' + inputType + '-TOTAL_FORMS').val(total);
        $('#id_' + inputType + '-MAX_NUM_FORMS').val(total);
    });
}

$('.add-more').on('click', function(event) {
    cloneMore($(this).prev('.question-group'));
});

$(document).on('click', '.delete-more', function() {
    $('a[data-toggle=popover]').popover('destroy');

    $(this).next('.question-group').remove();
    $(this).prev('.multiple-hr').remove();
    $(this).remove();

    $('a[data-toggle=popover]').popover();
});

function load_organization_template(){
    $('.radio-roles').on('change', function(){
     var template = $("#organization-template").html();
        $(this).parents('ul').after(template);
        $('#id_organization').remove();
    })
}

$( "#questionnaire_entry :input" ).change(function() {
  form_has_changed = true;
});

$("#questionnaire_entry").on('submit', function(){
    form_has_changed = false;
    this.submit();
});

function warn_before_navigating_away(){
    window.onbeforeunload = function(){
      if(form_has_changed){
        return "Are you sure you want to navigate away from this page?\nAll unsaved changes will be lost.";
       }
   };
};
