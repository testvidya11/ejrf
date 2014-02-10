from django.contrib import messages
from django.views.generic import CreateView
from questionnaire.forms.support_document_upload_form import SupportDocumentUploadForm
from questionnaire.models import SupportDocument, UserProfile, Questionnaire


class UploadDocument(CreateView):
    model = SupportDocument
    template_name = 'questionnaires/entry/upload.html'
    form_class = SupportDocumentUploadForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UploadDocument, self).get_context_data(**kwargs)
        questionnaire = self.kwargs['questionnaire_id']
        upload_data_initial = {'questionnaire': questionnaire}
        try:
            upload_data_initial.update({'country': self.request.user.user_profile.country})
        except UserProfile.DoesNotExist:
            pass
        context.update({'upload_form': self.form_class(initial=upload_data_initial), 'button_label': 'Upload'})
        return context

    def form_valid(self, form):
        messages.success(self.request, "File was uploaded successfully")
        return super(UploadDocument, self).form_valid(form)