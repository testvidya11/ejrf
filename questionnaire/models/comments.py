from django.contrib.auth.models import User
from questionnaire.models.base import BaseModel
from django.db import models


class Comment(BaseModel):
    text = models.CharField(max_length=100, blank=False, null=False)
    answer_group = models.ManyToManyField("AnswerGroup", blank=False, null=False, related_name="comments")
    user = models.ForeignKey(User, blank=False, null=False)