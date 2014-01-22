from django.utils.datastructures import SortedDict
from questionnaire.models import Question


class QuestionAnswerFormOrdering(object):

    def __init__(self, section, formsets):
        self.section = section
        self.formsets = formsets


    def ordered_forms(self):
        forms = SortedDict()
        counter = self._initialize_counter()
        for question in self.section.ordered_questions():
            forms[question]=self.formsets[question.answer_type][counter[question.answer_type]]
            counter[question.answer_type] += 1
        print forms
        return forms

    def _initialize_counter(self):
        return {key: 0 for key in [_type[0] for _type in Question.ANSWER_TYPES]}
