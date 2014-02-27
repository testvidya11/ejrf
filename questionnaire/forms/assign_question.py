from django.forms import Form
from django import forms
from questionnaire.models import Question


class AssignQuestionForm(Form):
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(), label='')

    def __init__(self, *args, **kwargs):
        self.subsection = kwargs.pop('subsection', None)
        super(AssignQuestionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True, *args, **kwargs):
        question_group = self.subsection.question_group.get_or_create()[0]
        args = list(self.cleaned_data['questions'])
        question_group.question.add(*args)
