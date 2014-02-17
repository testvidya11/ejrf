from django.forms import ModelForm
from django import forms
from questionnaire.models import Question


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['answer_type'].choices = self._set_answer_type_choices()

    class Meta:
        model = Question
        fields = ('text', 'instructions', 'short_instruction', 'answer_type', )
        widgets = {'text':  forms.Textarea(attrs={"rows": 6, "cols": 50}),
                   'instructions':  forms.Textarea(attrs={"rows": 6, "cols": 50}),
                   'short_instruction':  forms.Textarea(attrs={"rows": 2, "cols": 50})}

    def _set_answer_type_choices(self):
        choices = self.fields['answer_type'].choices
        choices[0] = ('', 'Answer type', )
        return choices

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit)
        if commit:
            question.UID = Question.next_uid()
            question.save()
        return question