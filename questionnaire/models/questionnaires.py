from questionnaire.models.base import BaseModel
from django.db import models


class Questionnaire(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=True)