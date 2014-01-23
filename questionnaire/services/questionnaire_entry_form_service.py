from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from django.forms.formsets import formset_factory

ANSWER_FORM ={
    'Number': NumericalAnswerForm,
    'Text': TextAnswerForm,
    'Date': DateAnswerForm,
    'MultiChoice': MultiChoiceAnswerForm
}


class QuestionnaireEntryFormService(object):

    def __init__(self, section):
        self.section = section
        self.ordered_questions = section.ordered_questions()
        self.formsets = self._formsets()
        self.ANSWER_FORM_COUNTER = self._initialize_form_counter()

    def next_ordered_form(self, question):
        next_question_type_count = self.ANSWER_FORM_COUNTER[question.answer_type]
        self.ANSWER_FORM_COUNTER[question.answer_type] += 1
        return self.formsets[question.answer_type][next_question_type_count]

    def _initialize_form_counter(self):
        return {key: 0 for key in ANSWER_FORM.keys()}


    def _formsets(self):
        formsets =  {}
        for answer_type in ANSWER_FORM.keys():
            questions = self.ordered_questions.filter(answer_type=answer_type)
            if questions:
                _formset_factory = formset_factory(ANSWER_FORM[answer_type], max_num=questions.count())
                initial = self._get_initial(questions)
                formsets[answer_type] = _formset_factory(initial=initial)
        return formsets

    def _get_initial(self, questions):
        return [{'question': question} for question in questions]
