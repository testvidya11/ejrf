from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from questionnaire.models import Question, QuestionOption


class QuestionForm(ModelForm):
    options = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer_type'].choices = self._set_answer_type_choices()

    class Meta:
        model = Question
        fields = ('text', 'instructions', 'short_instruction', 'answer_type', 'options')
        widgets = {'text':  forms.Textarea(attrs={"rows": 6, "cols": 50}),
                   'instructions':  forms.Textarea(attrs={"rows": 6, "cols": 50}),
                   'short_instruction':  forms.Textarea(attrs={"rows": 2, "cols": 50})}

    def clean(self):
        self._clean_options()
        return super(QuestionForm, self).clean()

    def _clean_options(self):
        answer_type = self.cleaned_data['answer_type']
        options = self.data.get('options', [])
        multichoice = 'MultiChoice'
        if answer_type == multichoice and options[0] == '':
            raise ValidationError("MultiChoice questions must have at least one option")
        return options

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit)
        if commit:
            question.UID = Question.next_uid()
            self._save_options_if_multichoice(question)
            question.save()
        return question

    def _save_options_if_multichoice(self, question):
        options = self.data.get('options', [])
        if options and question.answer_type == 'MultiChoice':
            for option in options:
                QuestionOption.objects.create(text=option, question=question)

    def _set_answer_type_choices(self):
        choices = self.fields['answer_type'].choices
        choices[0] = ('', 'Answer type', )
        return choices