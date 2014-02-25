$(function () {
    $('#select_survey_wizard-form').validate({
        rules: { 'questionnaire': 'required', 'year': 'required', 'name': 'required'}
    });

    var elementID = '#select_survey_wizard-form #id_questionnaire',
        selectQuestionnaireElement = $(elementID),
        questionnaireNameElement = $('#id_name');
    selectQuestionnaireElement.on('change', function () {
        questionnaireNameElement.val($(elementID + ' option:selected').text() + " Copy");
        questionnaireNameElement.attr('type', 'text').wrap("<p></p>").before("<label>New Questionnaire</label>");
    });

});
