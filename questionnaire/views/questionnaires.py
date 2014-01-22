from django.views.generic import FormView
from questionnaire.forms.questionnaire_entry import QuestionnaireEntryForm
from questionnaire.models import Questionnaire, Section
from questionnaire.services.question_answer_form_ordering import QuestionAnswerFormOrdering


class Entry(FormView):
    template_name = 'questionnaires/entry/index.html'

    def get(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        formsets = QuestionnaireEntryForm(section).formsets
        ordered_forms = QuestionAnswerFormOrdering(section, formsets)

        context = {'questionnaire': questionnaire, 'section': section,
                   'ordered_forms': ordered_forms}

        return self.render_to_response(context)

