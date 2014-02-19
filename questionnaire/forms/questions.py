from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from questionnaire.models import Question, QuestionOption


class QuestionForm(ModelForm):
    options = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer_type'].choices = self._set_answer_type_choices()
        self.fields['answer_type'].label = 'Response Type'
        self.fields['text'].label = 'Display label (Online)'
        self.fields['export_label'].label = 'Export label (Detail)'

    class Meta:
        model = Question
        fields = ('text', 'export_label', 'instructions', 'short_instruction', 'answer_type', 'options')
        widgets = {'text':  forms.Textarea(attrs={"rows": 6, "cols": 50}),
                   'instructions':  forms.Textarea(attrs={"rows": 6, "cols": 50}),
                   'short_instruction':  forms.Textarea(attrs={"rows": 2, "cols": 50}),
                   'answer_type': forms.Select(attrs={'class': 'form-control'}),
                   'export_label': forms.Textarea(attrs={"rows": 2, "cols": 50})}

    def clean(self):
        self._clean_options()
        self._clean_export_label()
        return super(QuestionForm, self).clean()

    def _clean_options(self):
        answer_type = self.data.get('answer_type', [])
        options = dict(self.data).get('options', [])
        options = [option for option in options if option]
        multichoice = 'MultiChoice'
        if (answer_type and answer_type == multichoice) and len(options) < 1:
            message = "MultiChoice questions must have at least one option"
            self._errors['answer_type'] = self.error_class([message])
            del self.cleaned_data['answer_type']
        return options

    def _clean_export_label(self):
        export_label = self.data.get('export_label', "")
        if not export_label:
            message = "All questions must have export label."
            self._errors['export_label'] = self.error_class([message])
            del self.cleaned_data['export_label']
        return export_label

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.UID = Question.next_uid()
        if commit:
            question.save()
            self._save_options_if_multichoice(question)
        return question

    def _save_options_if_multichoice(self, question):
        options = dict(self.data).get('options', [])
        if options and question.answer_type == 'MultiChoice':
            for option in options:
                QuestionOption.objects.create(text=option, question=question)

    def _set_answer_type_choices(self):
        choices = self.fields['answer_type'].choices
        choices[0] = ('', 'Response type', )
        return choices