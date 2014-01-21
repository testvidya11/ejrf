from django.forms import ModelForm
from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer


class NumericalAnswerForm(ModelForm):
    class Meta:
        model = NumericalAnswer

class TextAnswerForm(ModelForm):
    class Meta:
        model = TextAnswer

class DateAnswerForm(ModelForm):
    class Meta:
        model = DateAnswer

class MultiChoiceAnswerForm(ModelForm):
    class Meta:
        model = MultiChoiceAnswer
