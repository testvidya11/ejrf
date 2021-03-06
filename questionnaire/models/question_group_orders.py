from questionnaire.models.base import BaseModel
from django.db import models


class QuestionGroupOrder(BaseModel):
    question = models.ForeignKey("Question", blank=False, null=False, related_name="orders")
    order = models.PositiveIntegerField(blank=False, null=False)
    question_group = models.ForeignKey("QuestionGroup", blank=False, null=True, related_name="orders")

    class Meta:
        ordering = ('order',)
        app_label = 'questionnaire'
