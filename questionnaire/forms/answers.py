from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer, QuestionOption


class NumericalAnswerForm(ModelForm):

    class Meta:
        model = NumericalAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
            'code': forms.HiddenInput(),
        }

class TextAnswerForm(ModelForm):
    class Meta:
        model = TextAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
            'code': forms.HiddenInput(),
        }

class DateAnswerForm(ModelForm):
    class Meta:
        model = DateAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
            'code': forms.HiddenInput(),
        }


class MultiChoiceAnswerSelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=(), question_options=None):
        super(MultiChoiceAnswerSelectWidget, self).__init__(attrs, choices)
        self.question_options = question_options

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_text(option_value)
        data_instruction = ''
        if option_value:
            data_instruction = mark_safe(' data-instructions="%s"' % self.question_options.get(id=int(option_value)).instructions)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
        else:
            selected_html = ''
        return format_html('<option value="{0}"{1}{2}>{3}</option>',
                           option_value,
                           selected_html,
                           data_instruction,
                           force_text(option_label))


class MultiChoiceAnswerForm(ModelForm):
    response = ModelChoiceField(queryset=None, widget=forms.Select())

    def __init__(self, *args, **kwargs):
        super(MultiChoiceAnswerForm, self).__init__(*args, **kwargs)
        query_set = self._get_response_choices(kwargs)
        self.fields['response'].widget = self._get_response_widget(query_set)
        self.fields['response'].queryset = query_set
        self.fields['response'].empty_label = self._set_response_label(query_set)

    def _set_response_label(self, query_set):
        return None if query_set.count() <= 3 else "Choose One"

    def _get_response_widget(self, query_set):
        if query_set.count() <= 3:
            return forms.RadioSelect()
        if query_set.exclude(instructions=None).exists():
            return MultiChoiceAnswerSelectWidget(question_options=query_set)
        return forms.Select()

    def _get_response_choices(self, kwargs):
        if 'initial'in kwargs.keys() and 'question' in kwargs['initial'].keys():
            question = kwargs['initial']['question']
            return question.options.all()
        return QuestionOption.objects.all()


    class Meta:
        model = MultiChoiceAnswer

        widgets = {
            'question': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'country': forms.HiddenInput(),
            'version': forms.HiddenInput(),
            'code': forms.HiddenInput(),
        }

