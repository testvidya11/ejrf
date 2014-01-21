from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from django.forms.formsets import formset_factory

ANSWER_FORM ={
    'Number': NumericalAnswerForm,
    'Text': TextAnswerForm,
    'Date': DateAnswerForm,
    'MultiChoice': MultiChoiceAnswerForm
}


class QuestionnaireEntryForm(object):

    def __init__(self, section):
        self.section = section
        self.questions = section.all_questions()
        self.formsets = self._formsets()

    def _formsets(self):
        _formsets =  {}
        for answer_type in ANSWER_FORM.keys():
            count = self.questions.filter(answer_type=answer_type).count()
            if count:
                _formset_factory = formset_factory(ANSWER_FORM[answer_type], extra=count)
                _formsets[answer_type] = _formset_factory()
        return _formsets
