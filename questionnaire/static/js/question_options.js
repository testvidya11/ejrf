;
jQuery(function($){
    $("#id_options").remove();
    var $form = $("#id-new-question-form"),
        template = $("#question-option-template").html();

    function assignOptionNumbers(){
        $form.find("span.number").each(function(i, element){
            $(element).text(++i);
        });
    }

    function addQuestionOption($element){
        $element.before(template);
        assignOptionNumbers();
    }

    $('#id_answer_type').on('change', function(){
        if($(this).val() == 'MultiChoice'){
            $('#option-choices').addClass('show')
        }
    });

    $('input[type=radio]').on('change', function(){
        if($(this).val() == 'custom'){
            addQuestionOption($("div.form-actions"));
        }else{
            $form.find("div#option-input-group").remove();
        }
    });

    $form.on("click", ".add-option", function(){
        addQuestionOption($("div.form-actions"));
    });

    $form.on("click", ".remove-option", function(){
        $(this).parents("div#option-input-group").remove();
        assignOptionNumbers();
    });

    $
});