from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from questionnaire.forms.assign_question import AssignQuestionForm
from questionnaire.models import SubSection, Question
from braces.views import PermissionRequiredMixin


class AssignQuestion(View):
    template_name = "questionnaires/assign_questions.html"

    def get(self, request, *args, **kwargs):
        subsection = SubSection.objects.select_related('section').get(id=kwargs['subsection_id'])
        active_questions = subsection.section.questionnaire.get_all_questions()
        form = AssignQuestionForm(subsection=subsection)
        context= {'assign_question_form': form, 'active_questions': active_questions,
                  'btn_label': 'Done', 'questions': Question.objects.all() }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        referer_url = request.META.get('HTTP_REFERER', None)
        subsection = SubSection.objects.get(id=kwargs['subsection_id'])
        form = AssignQuestionForm(request.POST, subsection=subsection)
        if form.is_valid():
            form.save()
            messages.success(request, "Questions successfully assigned to questionnaire.")
            return HttpResponseRedirect(referer_url)
        context= {'assign_question_form': form,
                  'btn_label': 'Done', 'questions': form.fields['questions'].queryset }
        return render(request, self.template_name, context)
