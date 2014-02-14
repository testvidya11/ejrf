from django.forms import ModelForm
from django import forms
from questionnaire.models import Section


class SectionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Section
        fields = ['questionnaire', 'name', 'title', 'description']
        widgets = {'questionnaire': forms.HiddenInput(),
                   'description': forms.Textarea(attrs={"rows": 4, "cols": 50})}