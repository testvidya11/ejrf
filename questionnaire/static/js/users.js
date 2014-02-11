$(document).ready(function(){
    $('#id_organization').on('change', function(){
        getRegionsFor($(this), '#id_region');
    });
});

$(document).on('change', '#organization', function(){
    getRegionsFor(this, '#region');
});

function getRegionsFor(organization, region){
        var organization_id = $(organization).val(),
            url = "/locations/organization/"+ organization_id+"/region/",
            region_select = $(region);
        $.get(url, function(data){
            region_select.html(' ');
            region_select.html('<option value="">All </option>');
            data.forEach(function(region){
                region_select.append('<option value='+ region.id +'>'+ region.name +'</option>')
            });
        })
}

 var template = $("#organization-template").html(),
     country_template = $('#country-template').html(),
     region_template = $('#region-template').html();

function loadCountryAndRegionTemplate(country_template) {
    $(this).parents('ul').after(country_template);
}

function loadRoleTemplate(){
    $('.radio-roles').on('change', function(){
        removeHiddenFields.call(this);
        var $selected_role = $.trim($(this).parents('label').text()),
            select_element = $(this).parents('form').find('select');
            select_element.prev('label').remove();
            select_element.parents('p').remove();
        if($selected_role === "Global Admin"){
            loadCountryAndRegionTemplate.call(this, template);
        } else if ($selected_role == "Regional Admin") {
            loadCountryAndRegionTemplate.call(this, region_template);
        }else if ($selected_role == "Country Admin") {
            loadCountryAndRegionTemplate.call(this, country_template);
        }else if ($selected_role == "Data Submitter") {
            loadCountryAndRegionTemplate.call(this, country_template);
        }
    });
}

function removeHiddenFields(){
    $('#id_organization').remove();
    $('#id_region').remove();
    $('#id_country').remove();
}
