from django import forms
from django.contrib.auth.models import Group
from questionnaire.models import Region, Organization


class UserFilterForm(forms.Form):
    organization = forms.ModelChoiceField(queryset=Organization.objects.all().order_by('name'), empty_label="Select an Organisation",
                                    widget=forms.Select(attrs={"class": 'form-control'}))
    region = forms.ModelChoiceField(queryset=Region.objects.all().order_by('name'), empty_label="Select a region",
                                    widget=forms.Select(attrs={"class": 'form-control'}))
    role = forms.ModelChoiceField(queryset=Group.objects.all().order_by('name'), empty_label="Select a role ",
                                    widget=forms.Select(attrs={"class": 'form-control'}))