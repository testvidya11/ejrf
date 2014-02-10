from django.test import Client
from questionnaire.forms.support_document_upload_form import SupportDocumentUploadForm

from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Questionnaire


class UploadSupportDocumentTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user_with_no_permissions()
        self.login_user()

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)

    def test_get_upload_view(self):
        response = self.client.get('/questionnaire/entry/%s/documents/upload/' % self.questionnaire.id)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/upload.html', templates)
        self.assertEqual('Upload', response.context['button_label'])
        self.assertIsInstance(response.context['upload_form'], SupportDocumentUploadForm)