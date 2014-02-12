import os
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import CreateView, View
from django.views.static import serve
from questionnaire.forms.support_document_upload_form import SupportDocumentUploadForm
from questionnaire.models import SupportDocument, UserProfile, Questionnaire


class UploadDocument(CreateView):
    model = SupportDocument
    template_name = 'questionnaires/entry/upload.html'
    form_class = SupportDocumentUploadForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UploadDocument, self).get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.order_by('-created')[0]
        upload_data_initial = {'questionnaire': questionnaire}
        try:
            upload_data_initial.update({'country': self.request.user.user_profile.country})
        except UserProfile.DoesNotExist:
            pass
        context.update({'upload_form': self.form_class(initial=upload_data_initial),
                        'button_label': 'Upload', 'id': 'id-upload-form'})
        return context

    def form_valid(self, form):
        messages.success(self.request, "File was uploaded successfully")
        return super(UploadDocument, self).form_valid(form)

    def form_invalid(self, form):
        return render(self.request, self.template_name, {'upload_form': form,
                                                         'button_label': 'Upload', 'id': 'id-upload-form'})


class DownloadDocument(View):
    def get(self, *args, **kwargs):
        document = SupportDocument.objects.get(id=kwargs['document_id'], questionnaire=kwargs['questionnaire_id'])
        return serve(self.request, os.path.basename(document.path.url), os.path.dirname(document.path.url))