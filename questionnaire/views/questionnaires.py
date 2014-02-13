from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from django.forms.formsets import formset_factory
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from questionnaire.services.users import UserQuestionnaireService

ANSWER_FORM = {'Number': NumericalAnswerForm,
               'Text': TextAnswerForm,
               'Date': DateAnswerForm,
               'MultiChoice': MultiChoiceAnswerForm,
               }


class Entry(PermissionRequiredMixin, FormView):
    template_name = 'questionnaires/entry/index.html'
    permission_required = 'auth.can_submit_responses'
    def get(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        initial = {'status': 'Draft',}
        formsets = QuestionnaireEntryFormService(section, initial=initial)

        printable = False
        if 'printable' in request.GET:
            printable = True

        context = {'questionnaire': questionnaire, 'section': section, 'printable': printable,
                   'formsets': formsets, 'ordered_sections':Section.objects.order_by('order')}

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=self.kwargs['questionnaire_id'])
        section = Section.objects.get(id=self.kwargs['section_id'])
        user_questionnaire_service = UserQuestionnaireService(self.request.user, questionnaire)
        initial = {'country': self.request.user.user_profile.country, 'status': 'Draft',
                   'version': user_questionnaire_service.answer_version()}
        formsets = QuestionnaireEntryFormService(section, initial=initial, data=request.POST)

        context = {'questionnaire': questionnaire, 'section': section,
                   'formsets': formsets, 'ordered_sections': Section.objects.order_by('order')}

        if formsets.is_valid():
            return self._form_valid(request, formsets, user_questionnaire_service, context)
        return self._form_invalid(request, context)

    def _form_valid(self, request, formsets, user_questionnaire_service, context):
        formsets.save()
        message = 'Draft saved.'
        if 'final_submit' in request.POST:
            user_questionnaire_service.submit()
            message = 'Questionnaire Submitted.'
        messages.success(request, message)
        if request.POST.get('redirect_url', None):
            return HttpResponseRedirect(request.POST['redirect_url'])
        return self.render_to_response(context)

    def _form_invalid(self, request, context):
        message = 'Draft NOT saved. See errors below.'
        if 'final_submit' in request.POST:
            message = 'Submission NOT completed. See errors below.'
        messages.error(request, message)
        return self.render_to_response(context)
