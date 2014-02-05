var form_has_changed = false;

$(document).ready(function() {

    $('a[data-toggle=popover]').popover();
    load_role_template();
    $('p:empty').remove()
    warn_before_navigating_away();

    $('.datetimepicker').each(function(){
        $(this).datetimepicker({ pickTime: false });
    });
    
});

function cloneMore(selector) {
    $('a[data-toggle=popover]').popover('destroy');

    var newElement = $(selector).clone(true);
    updateFormCounts(newElement);

    newElement.find(':input').each(function() {
        // Reset cloned inputs
        if($(this).attr('type') != 'radio')
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

        var name = $(this).attr('name').replace(/-[\d]+-/g, '-'+total.toString()+'-');
        var id = $(this).attr('id').replace(/-[\d]+-/g, '-'+total.toString()+'-');
        $(this).attr({'name': name, 'id': id})

        if($(this).attr('type') == 'radio'){
            //update the previous label
            $(this).parents('label').attr({'for': id});
        }
        else
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

function load_country_and_region_template(country_template) {
    $(this).parents('ul').after(country_template);
    console.log($(this).next('p'))
}
function load_role_template(){
     var template = $("#organization-template").html(),
         country_template = $('#country-template').html(),
         region_template = $('#region-template').html();
    $('.radio-roles').on('change', function(){
        $('#id_organization').remove();
        $('#id_region').remove();
        $('#id_country').remove();
        var $selected_role = $.trim($(this).parents('label').text());
        var select_element = $(this).parents('form').find('select');
        select_element.prev('label').remove();
        select_element.parents('p').remove();

        if($selected_role === "Global Admin"){
            load_country_and_region_template.call(this, template);
        } else if ($selected_role == "Regional Admin") {
            load_country_and_region_template.call(this, region_template);
        }else if ($selected_role == "Country Admin") {
            load_country_and_region_template.call(this, country_template);
        }else if ($selected_role == "Data Submitter") {
            load_country_and_region_template.call(this, country_template);
        }
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
