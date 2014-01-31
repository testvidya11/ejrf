from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from questionnaire.models import NumericalAnswer, TextAnswer, DateAnswer, MultiChoiceAnswer, QuestionOption, AnswerGroup


class AnswerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self._initial = kwargs['initial'] if 'initial' in kwargs else {}
        self.question_group = self._initial['group'] if self._initial else None

    def save(self, commit=True, *args, **kwargs):
        answer = super(AnswerForm, self).save(commit=False, *args, **kwargs)
        self._add_extra_attributes_to(answer)
        answer.save()
        self._add_to_answer_group(answer)
        return answer

    def _add_extra_attributes_to(self, answer):
        for attribute in self._initial.keys():
            setattr(answer, attribute, self._initial[attribute])

    def _add_to_answer_group(self, answer):
        answer_group = AnswerGroup.objects.get_or_create(grouped_question=self.question_group)[0]
        answer_group.answer.add(answer)

class NumericalAnswerForm(AnswerForm):
    class Meta:
        model = NumericalAnswer
        exclude = ('question', 'status', 'country', 'version', 'code')

class TextAnswerForm(AnswerForm):
    class Meta:
        model = TextAnswer
        exclude = ('question', 'status', 'country', 'version', 'code')

class DateAnswerForm(AnswerForm):
    class Meta:
        model = DateAnswer
        exclude = ('question', 'status', 'country', 'version', 'code')


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


class MultiChoiceAnswerForm(AnswerForm):
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
        exclude = ('question', 'status', 'country', 'version', 'code')
