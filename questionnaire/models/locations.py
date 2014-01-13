from questionnaire.models.base import BaseModel
from django.db import models


class LocationType(BaseModel):
    order = models.PositiveIntegerField(max_length=2, blank=False, null=True, unique=True)
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
