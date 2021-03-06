from django.db import models
from questionnaire.models.base import BaseModel
from questionnaire.utils.question_util import largest_uid, stringify


class Question(BaseModel):

    NUMBER = "Number"
    MULTICHOICE = "MultiChoice"
    ANSWER_TYPES = (
        ("Date", "Date"),
        ("MultiChoice", MULTICHOICE),
        ("Number", NUMBER),
        ("Text", "Text"),
    )

    text = models.TextField(blank=False, null=False)
    export_label = models.TextField(blank=True, null=False)
    instructions = models.TextField(blank=True, null=True)
    UID = models.CharField(blank=False, null=False, max_length=6, unique=True)
    answer_type = models.CharField(blank=False, null=False, max_length=20, choices=ANSWER_TYPES)
    is_core = models.BooleanField(blank=False, null=False, default=False)
    is_primary = models.BooleanField(blank=False, null=False, default=False)
    is_required = models.BooleanField(blank=False, null=False, default=False)

    def all_answers(self):
        return self.answers.filter(status='Submitted').order_by('answergroup__id').select_subclasses()

    def __unicode__(self):
        return "%s" % self.text

    def group(self):
        return self.question_group.all()[0]

    def is_first_in_group(self):
        questions = self.group().ordered_questions()
        return self == questions[0]

    def is_last_in_group(self):
        questions = self.group().ordered_questions()
        return self == questions[-1]

    def has_question_option_instructions(self):
        return self.options.exclude(instructions=None)

    def latest_answer(self, parent_group, country):
        answer = self.answers.filter(answergroup__grouped_question=parent_group,
                                     country=country).select_subclasses()
        if answer.exists():
            return answer.latest('modified')
        return None

    def is_in_subgroup(self):
        return self.question_group.exclude(parent=None).exists()

    def can_be_deleted(self):
        return not self.all_answers().exists()

    def get_option_at(self, index=1):
        if self.is_primary:
            all_options = self.options.order_by('text')
            return all_options[index - 1]

    def get_initial(self, order, option_index=1, country=None):
        answer = self.latest_answer(order.question_group, country)
        initial = {'question': self, 'group': order.question_group, 'country': country}
        if self.is_primary and order.question_group.grid and order.question_group.display_all:
            initial['response'] = self.get_option_at(option_index)
        if answer and answer.is_draft():
            initial['answer'] = answer
            initial['response'] = answer.format_response()
        return initial

    def is_assigned_to(self, questionnaire):
        return self.question_group.filter(subsection__section__questionnaire=questionnaire).exists()

    @classmethod
    def next_uid(cls):
        return stringify(largest_uid(cls) + 1)


class QuestionOption(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question, related_name="options")
    instructions = models.TextField(blank=True, null=True)
    UID = models.CharField(blank=False, max_length=6, unique=True, null=True)

    def __unicode__(self):
        return "%s" % self.text