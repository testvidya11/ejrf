from django.forms import ModelForm
from questionnaire.models import NumericalAnswer, TextAnswer


class NumericalAnswerForm(ModelForm):
    class Meta:
        model = NumericalAnswer

class TextAnswerForm(ModelForm):
    class Meta:
        model = TextAnswer
