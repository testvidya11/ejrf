from questionnaire.models.base import BaseModel
from django.db import models


class Region(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

