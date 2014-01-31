from django.contrib.auth.models import User
from questionnaire.models.base import BaseModel
from django.db import models


class UserProfile(BaseModel):
    user = models.OneToOneField(User, related_name="user_profile")
    region = models.ForeignKey("Region", blank=True, null=True)
    country = models.ForeignKey("Country", blank=True, null=True)
    organization = models.ForeignKey("Organization", blank=True, null=True)