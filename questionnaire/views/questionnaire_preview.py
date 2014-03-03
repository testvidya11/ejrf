from django.shortcuts import render
from django.views.generic import View
from questionnaire.models import Questionnaire
from questionnaire.services.users import UserQuestionnaireService
from braces.views import PermissionRequiredMixin, MultiplePermissionsRequiredMixin


class PreviewQuestionnaire(MultiplePermissionsRequiredMixin, View):
    template_name = "questionnaires/entry/preview.html"

    permissions = {
        "any" : ("auth.can_submit_responses", "auth.can_view_questionnaire"),
    }

    def get(self, request, *args, **kwargs):
        if kwargs.get('questionnaire_id'):
            questionnaire = Questionnaire.objects.get(id=kwargs.get('questionnaire_id'))
        else:
            questionnaire = Questionnaire.objects.get(status=Questionnaire.PUBLISHED)
        user_questionnaire_service = UserQuestionnaireService(self.request.user, questionnaire)
        context = {'all_sections_questionnaires': user_questionnaire_service.all_sections_questionnaires(),
                   'ordered_sections': questionnaire.sections.order_by('order')}
        return render(request, self.template_name, context)
