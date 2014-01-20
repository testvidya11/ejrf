from questionnaire.models.base import BaseModel
from django.db import models


class QuestionGroupOrder(BaseModel):
    question = models.ForeignKey("Question", blank=False, null=False)
    order = models.PositiveIntegerField(blank=False, null=False)
    question_group = models.ForeignKey("QuestionGroup", blank=False, null=True)