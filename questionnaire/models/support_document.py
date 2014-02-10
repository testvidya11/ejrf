from django.db import models

from eJRF.settings import UPLOADS_MEDIA_URL
from questionnaire.models import Questionnaire
from questionnaire.models.base import BaseModel


class SupportDocument(BaseModel):
    questionnaire = models.ForeignKey(Questionnaire, blank=False, null=False, related_name="support_documents")
    country = models.ForeignKey('Country', blank=False, null=False)
    path = models.FileField(upload_to=UPLOADS_MEDIA_URL)