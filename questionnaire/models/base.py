from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    class Meta:
        app_label = 'questionnaire'
        abstract = True