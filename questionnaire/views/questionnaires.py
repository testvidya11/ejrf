from django.views.generic import FormView
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section


class Entry(FormView):
    template_name = 'questionnaires/entry/index.html'

    def get(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        formsets = QuestionnaireEntryFormService(section)

        context = {'questionnaire': questionnaire, 'section': section,
                   'formsets': formsets, 'ordered_sections':Section.objects.order_by('order')}

        return self.render_to_response(context)

