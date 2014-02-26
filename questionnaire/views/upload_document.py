import os
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, View
from django.views.static import serve
from questionnaire.forms.support_documents import SupportDocumentUploadForm
from questionnaire.models import SupportDocument, Questionnaire


class UploadDocument(CreateView):
    model = SupportDocument
    template_name = 'questionnaires/entry/upload.html'
    form_class = SupportDocumentUploadForm
    success_url = '/questionnaire/documents/upload/'

    def get_context_data(self, **kwargs):
        context = super(UploadDocument, self).get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.all().latest('created')
        users_country = self.request.user.user_profile.country
        upload_data_initial = {'questionnaire': questionnaire, 'country': users_country}
        context.update({'upload_form': self.form_class(initial=upload_data_initial),
                        'button_label': 'Upload', 'id': 'id-upload-form', 'questionnaire': questionnaire,
                        'documents': self.model.objects.filter(country=users_country)})
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


class DeleteDocument(View):
    model = SupportDocument

    def get(self, *args, **kwargs):
        document = self.model.objects.get(pk=kwargs['document_id'])
        os.system("rm %s" % document.path.url)
        document.delete()
        messages.success(self.request, "Attachment was deleted successfully")
        return HttpResponseRedirect(reverse_lazy('upload_document'))