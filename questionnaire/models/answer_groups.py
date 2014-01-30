from questionnaire.models import Answer
from questionnaire.models.base import BaseModel
from django.db import models


class AnswerGroup(BaseModel):
    answer = models.ManyToManyField(Answer, null=True)
    grouped_question = models.ForeignKey("QuestionGroup", null=True, related_name="answer_groups")
    row = models.CharField(max_length=6)