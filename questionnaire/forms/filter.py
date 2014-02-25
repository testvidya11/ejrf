from datetime import date
from django import forms
from django.contrib.auth.models import Group
from questionnaire.models import Region, Organization, Questionnaire


class UserFilterForm(forms.Form):
    organization = forms.ModelChoiceField(queryset=Organization.objects.all().order_by('name'),
                                          empty_label="All",
                                          widget=forms.Select(attrs={"class": 'form-control region-select'}),
                                          required=False)
    region = forms.ModelChoiceField(queryset=Region.objects.all(), empty_label="All",
                                    widget=forms.Select(attrs={"class": 'form-control region-select'}), required=False)
    role = forms.ModelChoiceField(queryset=Group.objects.all().order_by('name'), empty_label="All",
                                  widget=forms.Select(attrs={"class": 'form-control region-select'}), required=False)


class QuestionnaireFilterForm(forms.Form):
    questionnaire = forms.ModelChoiceField(queryset=Questionnaire.objects.filter(finalized=True), empty_label="All",
                                           widget=forms.Select(attrs={"class": 'form-control'}), required=True)
    year = forms.ChoiceField(widget=forms.Select(attrs={"class": 'form-control'}), required=False, choices=[])
    name = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(QuestionnaireFilterForm, self).__init__(*args, **kwargs)
        self.fields['year'].choices = self._set_year_choices()

    def _set_year_choices(self):
        choices = []
        choices.insert(0, ('', 'Choose a year', ))
        choices.extend((year, year) for year in list([date.today().year + count for count in range(0, 10)]))
        return choices