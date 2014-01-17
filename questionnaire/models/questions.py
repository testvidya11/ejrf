from questionnaire.models.base import BaseModel
from django.db import models

class Question(BaseModel):

    ANSWER_TYPES = (
        ("Date","Date"),
        ("MultiChoice","MultiChoice"),
        ("Number","Number"),
        ("Text","Text"),
    )

    text = models.TextField(blank=False, null=False)
    instructions = models.TextField(blank=False, null=True)
    UID = models.CharField(blank=False, null=False, max_length=6)
    answer_type = models.CharField(blank=False, null=False, max_length=10, choices=ANSWER_TYPES)



