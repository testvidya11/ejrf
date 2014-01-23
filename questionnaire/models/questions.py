from django.db import models
from questionnaire.models.base import BaseModel


class Question(BaseModel):

    ANSWER_TYPES = (
        ("Date", "Date"),
        ("MultiChoice", "MultiChoice"),
        ("Number", "Number"),
        ("Text", "Text"),
    )

    text = models.TextField(blank=False, null=False)
    instructions = models.TextField(blank=False, null=True)
    short_instruction = models.CharField(max_length=250, blank=False, null=True)
    UID = models.CharField(blank=False, null=False, max_length=6, unique=True)
    answer_type = models.CharField(blank=False, null=False, max_length=20, choices=ANSWER_TYPES)

    def all_answers(self):
        return self.answers.filter(status='Submitted').order_by('created').select_subclasses()

    def __unicode__(self):
        return "%s" % self.text


class QuestionOption(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    question = models.ForeignKey(Question, related_name="options")

    def __unicode__(self):
        return "%s" % self.text