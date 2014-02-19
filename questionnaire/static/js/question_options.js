;
jQuery(function($){
    $("#id_options").remove();
    var $form = $("#id-new-question-form"),
        template = $("#question-option-template").html(),
        answerTypeSelect = $('#id_answer_type');
        answerTypeSelect.prop('selectedIndex',0);
    function assignOptionNumbers(){
        $form.find("span.number").each(function(i, element){
            $(element).text(++i);
        });
    }

    function addQuestionOption($element){
        $element.before(template);
        assignOptionNumbers();
    }

    answerTypeSelect.on('change', function(){
        if($(this).val() == 'MultiChoice'){
            $('#option-choices').addClass('show').removeClass('hide')
        }else{
            $('#option-choices').removeClass('show').addClass('hide')
        }
    });

    $('input[type=radio]').on('change', function(){
        if($(this).val() == 'custom'){
            addQuestionOption($("div.form-actions"));
            $form.find('input[name=options]').prop('checked', false)
        }else{
            $form.find("div#option-input-group").remove();
            $form.find('input[name=options-custom]').prop('checked', false)
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