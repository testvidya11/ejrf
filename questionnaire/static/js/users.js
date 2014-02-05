$('#id_organization').on('change', function(){
    var organization_id = $(this).val(),
        url = "/locations/organization/"+ organization_id+"/region/",
        region_select = $('#id_region');
    $.get(url, function(data){
        region_select.html(' ');
        data.forEach(function(region){
            region_select.append('<option value='+ region.id +'>'+ region.name +'</option>')
        });
    })
});