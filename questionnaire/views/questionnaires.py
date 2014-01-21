from django.views.generic import FormView
from questionnaire.models import Questionnaire, Section


class Entry(FormView):
    template_name = 'questionnaires/entry/index.html'

    def get(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        context = {'questionnaire': questionnaire, 'section': section}

        return self.render_to_response(context)

