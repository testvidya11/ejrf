from django.db import models
from questionnaire.models.base import BaseModel


class QuestionTextHistory(BaseModel):
    text = models.TextField(blank=False, null=False)
    export_label = models.TextField(blank=True, null=False)
    questionnaire = models.ForeignKey("Questionnaire", blank=False, null=False)
    question = models.ForeignKey("Question", blank=False, null=False, related_name="history")