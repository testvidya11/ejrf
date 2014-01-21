from django.forms import ModelForm
from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer


class NumericalAnswerForm(ModelForm):
    class Meta:
        model = NumericalAnswer

class TextAnswerForm(ModelForm):
    class Meta:
        model = TextAnswer

class DateAnswerForm(ModelForm):
    class Meta:
        model = DateAnswer
