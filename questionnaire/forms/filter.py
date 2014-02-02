from django import forms
from questionnaire.models import Region


class UserFilterForm(forms.Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all().order_by('name'), empty_label=None)