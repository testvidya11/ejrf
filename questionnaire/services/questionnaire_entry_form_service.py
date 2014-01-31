from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from django.forms.formsets import formset_factory

ANSWER_FORM ={
    'Number': NumericalAnswerForm,
    'Text': TextAnswerForm,
    'Date': DateAnswerForm,
    'MultiChoice': MultiChoiceAnswerForm
}


class QuestionnaireEntryFormService(object):

    def __init__(self, section, initial={}, data=None):
        self.initial = initial
        self.data = data
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
        formsets = {}
        for answer_type in ANSWER_FORM.keys():
            questions = filter(lambda question: question.answer_type == answer_type, self.ordered_questions)
            if questions:
                _formset_factory = formset_factory(ANSWER_FORM[answer_type], max_num=len(questions))
                initial = self._get_initial(questions)
                formsets[answer_type] = _formset_factory(prefix=answer_type, initial=initial, data=self.data)
        return formsets

    def _get_initial(self, questions):
        return [dict(self.initial.items() + {'question': question}.items())  for question in questions]

    def is_valid(self):
        formset_checks = [formset.is_valid() for formset in self.formsets.values()]
        return len(formset_checks) == formset_checks.count(True)

    def save(self):
        for formset in self.formsets.values():
            for form in formset:
                form.save()

