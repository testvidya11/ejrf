from questionnaire.models.base import BaseModel
from django.db import models


class QuestionGroup(BaseModel):
    question = models.ManyToManyField("Question", blank=False, null=False)
    subsection = models.ForeignKey("SubSection", blank=False, null=False)
    order = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=True)
    instructions = models.TextField(blank=False, null=True)
