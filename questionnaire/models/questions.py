import re
from django.db import models
from questionnaire.models.base import BaseModel

INITIAL_UID = 1

MAX_UID_LENGTH = 5


class Question(BaseModel):

    ANSWER_TYPES = (
        ("Date", "Date"),
        ("MultiChoice", "MultiChoice"),
        ("Number", "Number"),
        ("Text", "Text"),
    )

    text = models.TextField(blank=False, null=False)
    export_label = models.TextField(blank=True, null=False)
    instructions = models.TextField(blank=False, null=True)
    short_instruction = models.CharField(max_length=250, blank=False, null=True)
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

    def draft_answer(self, parent_group, country):
        from questionnaire.models import Answer
        answer = self.answers.filter(answergroup__grouped_question=parent_group,
                                     status=Answer.DRAFT_STATUS, country=country).select_subclasses()
        if answer.exists():
            return answer.latest('modified')
        return None

    @classmethod
    def largest_uid(cls):
        uid_numbers = []
        all_question_uids = Question.objects.all().values_list('UID', flat=True)
        for uid in all_question_uids:
            uid_numbers.extend([int(num[0]) for num in re.findall(r'(\d+)|([\+-]?\d+)', uid)])
        return max(uid_numbers) if len(uid_numbers) > 0 else INITIAL_UID

    @classmethod
    def next_uid(cls):
        largest_uid = cls.largest_uid()
        return cls.stringify(largest_uid + 1)

    @classmethod
    def stringify(cls, uid):
        return "0" * (MAX_UID_LENGTH - len(str(uid))) + str(uid)


class QuestionOption(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question, related_name="options")
    instructions = models.TextField(blank=True, null=True)
    UID = models.CharField(blank=False, max_length=6, unique=True, null=True)

    def __unicode__(self):
        return "%s" % self.text