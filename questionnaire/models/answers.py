from questionnaire.models.questions import Question
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