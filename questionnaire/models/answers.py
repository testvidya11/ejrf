from questionnaire.models.questions import Question, QuestionOption
from questionnaire.models.base import BaseModel
from django.db import models


class Answer(BaseModel):
    DRAFT_STATUS = "Draft"
    SUBMITTED_STATUS = 'Submitted'
    STATUS_CHOICES = {
        ("DRAFT", DRAFT_STATUS),
        ("SUBMITTED", SUBMITTED_STATUS),
    }

    question = models.ForeignKey(Question, null=True)
    country = models.ForeignKey("Country", null=True)
    status = models.CharField(max_length=15, blank=False, null=False, choices=STATUS_CHOICES, default=DRAFT_STATUS)
    version = models.IntegerField(blank=False, null=True, default=1)


class NumericalAnswer(Answer):
    response = models.DecimalField(max_digits=5, decimal_places=2)


class TextAnswer(Answer):
    response = models.CharField(max_length=100, null=True)


class DateAnswer(Answer):
    response = models.DateField()


class MultiChoiceAnswer(Answer):
    response = models.ForeignKey(QuestionOption)