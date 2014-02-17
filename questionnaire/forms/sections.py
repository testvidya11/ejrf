from django.forms import ModelForm
from django import forms
from questionnaire.models import Section, SubSection


class SectionForm(ModelForm):

    class Meta:
        model = Section
        fields = ['questionnaire', 'name', 'title', 'description']
        widgets = {'questionnaire': forms.HiddenInput(),
                   'description': forms.Textarea(attrs={"rows": 4, "cols": 50})}

class SubSectionForm(ModelForm):
    class Meta:
        model = SubSection
        fields = ['title', 'description']
        widgets = {
                   'description': forms.Textarea(attrs={"rows": 4, "cols": 50})}
