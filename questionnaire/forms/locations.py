from django.forms import ModelForm
from questionnaire.models import LocationType


class LocationTypeForm(ModelForm):
    class Meta:
        model = LocationType
