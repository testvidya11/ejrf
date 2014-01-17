from questionnaire.models.questions import Question, QuestionOption
from questionnaire.models.base import BaseModel
from django.db import models


class Answer(BaseModel):
    question = models.ForeignKey(Question, null=True)
    country = models.ForeignKey("Country", null=True)

    class Meta:
        app_label = 'questionnaire'
        abstract = True


class NumericalAnswer(Answer):
    response = models.DecimalField(max_digits=5, decimal_places=2)


class TextAnswer(Answer):
    response = models.CharField(max_length=100, null=True)


class DateAnswer(Answer):
    response = models.DateField()


class MultiChoiceAnswer(Answer):
    response = models.ForeignKey(QuestionOption)