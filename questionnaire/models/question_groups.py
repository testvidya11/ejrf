from questionnaire.models.base import BaseModel
from django.db import models


class QuestionGroup(BaseModel):
    question = models.ManyToManyField("Question", blank=False, null=False)
    subsection = models.ForeignKey("SubSection", blank=False, null=False, related_name="question_group")
    name = models.CharField(max_length=200, blank=False, null=True)
    instructions = models.TextField(blank=False, null=True)
    parent = models.ForeignKey("QuestionGroup", null=True)
    order = models.PositiveIntegerField(null=True, blank=False)

    def all_questions(self):
        return self.question.all()
