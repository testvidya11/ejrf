from questionnaire.models.base import BaseModel
from django.db import models

class Location(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=True)

    class Meta:
        abstract = True
        app_label = 'questionnaire'


class Region(Location):
    description = models.CharField(max_length=300, blank=True, null=True)


class Country(Location):
    region = models.ForeignKey(Region, blank=False, null=True, related_name="countries")