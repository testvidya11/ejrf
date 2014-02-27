from django.shortcuts import render
from django.views.generic import View
from questionnaire.forms.assign_question import AssignQuestionForm
from questionnaire.models import SubSection
from braces.views import PermissionRequiredMixin


class AssignQuestion(View):
    template_name = "questionnaires/assign_questions.html"

    def get(self, request, *args, **kwargs):
        subsection = SubSection.objects.get(id=kwargs['subsection_id'])
        form = AssignQuestionForm(subsection=subsection)
        context= {'assign_question_form': form,
                  'btn_label': 'Done', 'questions': form.fields['questions'].queryset }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        subsection = SubSection.objects.get(id=kwargs['subsection_id'])
        form = AssignQuestionForm(request.POST, subsection=subsection)
        if form.is_valid():
            form.save()
        context= {'assign_question_form': form,
                  'btn_label': 'Done', 'questions': form.fields['questions'].queryset }
        return render(request, self.template_name, context)
