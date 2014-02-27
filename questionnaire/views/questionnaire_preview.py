from django.shortcuts import render
from django.views.generic import View
from questionnaire.models import Questionnaire
from questionnaire.services.users import UserQuestionnaireService
from braces.views import PermissionRequiredMixin


class PreviewQuestionnaire(PermissionRequiredMixin, View):
    template_name = "questionnaires/entry/preview.html"
    permission_required = "auth.can_submit_responses"

    def get(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(status=Questionnaire.PUBLISHED)
        user_questionnaire_service = UserQuestionnaireService(self.request.user, questionnaire)
        context = {'all_sections_questionnaires': user_questionnaire_service.all_sections_questionnaires(),
                   'ordered_sections': questionnaire.sections.order_by('order')}
        return render(request, self.template_name, context)
