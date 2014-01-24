from django.contrib.auth.models import User
from questionnaire.models.base import BaseModel
from django.db import models


class UserProfile(BaseModel):
    user = models.OneToOneField(User, related_name="user_profile")
    region = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)