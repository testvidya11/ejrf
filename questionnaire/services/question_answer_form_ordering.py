from django.utils.datastructures import SortedDict
from questionnaire.models import Question


class QuestionAnswerFormOrdering(object):

    def __init__(self, section, formsets):
        self.section = section
        self.formsets = formsets

    def get_ordered_questions(self):
        subsections = self.section.sub_sections.order_by('order')
        questions = []
        for subsection in subsections:
            for group in subsection.question_group.order_by('order'):
                questions.extend(group.orders.order_by('order').values_list('question', flat=True))

        return Question.objects.filter(id__in=questions)

    def ordered_forms(self):
        forms = SortedDict()
        counter = self._initialize_counter()
        for question in self.get_ordered_questions():
            forms[question]=self.formsets[question.answer_type][counter[question.answer_type]]
            forms[question].initial = {'question':question}
            counter[question.answer_type] += 1
        return forms

    def _initialize_counter(self):
        return {key: 0 for key in [_type[0] for _type in Question.ANSWER_TYPES]}
