from django.forms import ModelForm
from questionnaire.models import NumericalAnswer


class NumericalAnswerForm(ModelForm):
    class Meta:
        model = NumericalAnswer
