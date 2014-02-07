from questionnaire.models import Questionnaire
from django.db import models
from questionnaire.models.base import BaseModel


class SupportDocument(BaseModel):
    questionnaire = models.ForeignKey(Questionnaire)
    country = models.ForeignKey('Country')
    path = models.FileField(upload_to='.')