from questionnaire.models import Questionnaire
from questionnaire.models.base import BaseModel
from django.db import models


class Section(BaseModel):
    title = models.CharField(max_length=256, blank=False, null=False)
    order = models.IntegerField(blank=False, null=False)
    questionnaire = models.ForeignKey(Questionnaire, blank=False, null=False, related_name="sections")


class SubSection(BaseModel):
    title = models.CharField(max_length=256, blank=False, null=False)
    order = models.IntegerField(blank=False, null=False)
    section = models.ForeignKey(Section, blank=False, null=False, related_name="sub_sections")
    description = models.TextField(blank=True, null=True)
