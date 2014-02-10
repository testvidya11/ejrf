import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from mock import mock_open, patch
from questionnaire.forms.support_document_upload_form import SupportDocumentUploadForm

from questionnaire.tests.base_test import BaseTest
from questionnaire.models import Questionnaire, Country


class UploadSupportDocumentTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()
        self.login_user()
        self.filename = 'empty_file.pdf'
        self.uganda = Country.objects.create(name="Uganda")
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)

    def test_get_upload_view(self):
        response = self.client.get('/questionnaire/entry/%s/documents/upload/' % self.questionnaire.id)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/upload.html', templates)
        self.assertEqual('Upload', response.context['button_label'])
        self.assertIsInstance(response.context['upload_form'], SupportDocumentUploadForm)

    def test_upload_upload(self):
        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            document = open(self.filename, 'rb')
        data = {'questionnaire': self.questionnaire.id, 'country': self.uganda.id, 'path': document}
        response = self.client.post('/questionnaire/entry/%s/documents/upload/' % self.questionnaire.id, data=data)
        self.assertRedirects(response, '/', status_code=302)
        message = "File was uploaded successfully"
        self.assertIn(message, response.cookies['messages'].value)

    def test_user_does_not_exist_upload_upload(self):
        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            document = open(self.filename, 'rb')
        data = {'questionnaire': self.questionnaire.id, 'country': '', 'path': document}
        response = self.client.post('/questionnaire/entry/%s/documents/upload/' % self.questionnaire.id, data=data)
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        os.system("rm -rf %s" % self.filename)
