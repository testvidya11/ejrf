from questionnaire.models import Answer
from questionnaire.models.base import BaseModel
from django.db import models


class GroupedAnswer(BaseModel):
    answer = models.ForeignKey(Answer, null=True)
    grouped_question = models.ForeignKey("GroupedQuestion", null=True)
    row = models.CharField(max_length=6)