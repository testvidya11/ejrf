from django import forms
from django.forms import ModelForm
from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer, QuestionOption


class NumericalAnswerForm(ModelForm):

    class Meta:
        model = NumericalAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
        }

class TextAnswerForm(ModelForm):
    class Meta:
        model = TextAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
        }

class DateAnswerForm(ModelForm):
    class Meta:
        model = DateAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
        }


class MultiChoiceAnswerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MultiChoiceAnswerForm, self).__init__(*args, **kwargs)
        self.fields['response'].queryset = self._get_response_choices(kwargs)
        self.fields['response'].empty_label = None


    def _get_response_choices(self, kwargs):
        if 'initial'in kwargs.keys() and 'question' in kwargs['initial'].keys():
            return kwargs['initial']['question'].options.all()
        return QuestionOption.objects.all()


    class Meta:
        model = MultiChoiceAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
        }
