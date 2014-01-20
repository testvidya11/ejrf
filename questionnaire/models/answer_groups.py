from questionnaire.models import Answer
from questionnaire.models.base import BaseModel
from django.db import models


class AnswerGroup(BaseModel):
    answer = models.ForeignKey(Answer, null=True)
    grouped_question = models.ForeignKey("QuestionGroup", null=True)
    row = models.CharField(max_length=6)