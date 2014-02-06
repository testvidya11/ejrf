$(document).ready(function(){
    $('#id_organization').on('change', function(){
        get_regions_for($(this), '#id_region');
    });
});

$(document).on('change', '#organization', function(){
    get_regions_for(this, '#region');
});

function get_regions_for(organization, region){
        var organization_id = $(organization).val(),
            url = "/locations/organization/"+ organization_id+"/region/",
            region_select = $(region);
        $.get(url, function(data){
            region_select.html(' ');
            region_select.html('<option>Select a region </option>');
            data.forEach(function(region){
                region_select.append('<option value='+ region.id +'>'+ region.name +'</option>')
            });
        })
}

 var template = $("#organization-template").html(),
     country_template = $('#country-template').html(),
     region_template = $('#region-template').html();

function load_country_and_region_template(country_template) {
    $(this).parents('ul').after(country_template);
}

function load_role_template(){
    $('.radio-roles').on('change', function(){
        remove_hidden_fields.call(this);
        var $selected_role = $.trim($(this).parents('label').text()),
            select_element = $(this).parents('form').find('select');
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
    });
}

function remove_hidden_fields(){
    $('#id_organization').remove();
    $('#id_region').remove();
    $('#id_country').remove();
}
