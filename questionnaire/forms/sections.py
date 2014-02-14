from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from questionnaire.models import Section


class SectionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Section
        fields = ['questionnaire', 'name', 'title', 'description']
        widgets = {'questionnaire': forms.HiddenInput()}

    def clean_order(self):
        order = self.cleaned_data['order']
        questionnaire = self.cleaned_data['questionnaire']
        if Section.objects.filter(order=order, questionnaire=questionnaire).exists():
            raise ValidationError("Orders should be unique")
        return order