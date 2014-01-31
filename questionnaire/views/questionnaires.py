from django.views.generic import FormView
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from django.forms.formsets import formset_factory
from braces.views import LoginRequiredMixin

ANSWER_FORM ={
            'Number': NumericalAnswerForm,
            'Text': TextAnswerForm,
            'Date': DateAnswerForm,
            'MultiChoice': MultiChoiceAnswerForm
        }
class Entry(LoginRequiredMixin, FormView):
    template_name = 'questionnaires/entry/index.html'

    def get(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        formsets = QuestionnaireEntryFormService(section)

        context = {'questionnaire': questionnaire, 'section': section,
                   'formsets': formsets, 'ordered_sections':Section.objects.order_by('order')}

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        initial = {'country': self.request.user.user_profile.country, 'status': 'Draft', 'version':1, 'code':'ABC123'}
        formsets = QuestionnaireEntryFormService(section, initial=initial, data=request.POST)

        if formsets.is_valid():
            return self._form_valid(formsets, questionnaire, section)
        return self._form_invalid(formsets)

    def _form_valid(self, formsets, questionnaire, section):
        formsets.save()
        context = {'questionnaire': questionnaire, 'section': section,
                   'formsets': formsets, 'ordered_sections': Section.objects.order_by('order')}

        return self.render_to_response(context)


    def _form_invalid(self, formsets):

        pass