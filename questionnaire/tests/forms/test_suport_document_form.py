import os
from mock import mock_open, patch, Mock
from django.core.files.uploadedfile import SimpleUploadedFile
from eJRF.settings import ACCEPTED_EXTENSIONS, FILE_SIZE_LIMIT
from questionnaire.forms.support_document_upload_form import SupportDocumentUploadForm
from questionnaire.tests.base_test import BaseTest


class SupportDocumentTest(BaseTest):
    def setUp(self):
        self.filename = 'empty_file'

    def tearDown(self):
        os.system("rm -rf %s" % self.filename)

    def test_should_know_fields(self):
        upload_form = SupportDocumentUploadForm()

        fields = ['file']

        [self.assertIn(field, upload_form.fields) for field in fields]

    def test_empty_file(self):
        data_file = {'file': SimpleUploadedFile(self.filename, open(self.filename, 'a').close())}

        upload_document_form = SupportDocumentUploadForm({}, data_file)
        self.assertFalse(upload_document_form.is_valid())
        self.assertIn('The submitted file is empty.', upload_document_form.errors['file'])

    def test_not_allowed_extension(self):
        self.filename = 'executable_file.exe'
        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            document = open(self.filename, 'rb')
            file_data = {'file': SimpleUploadedFile(self.filename, document.read())}
            upload_document_form = SupportDocumentUploadForm({}, file_data)
            self.assertFalse(upload_document_form.is_valid())
            error_message = ".exe file type is not an allowed, Please upload %s files only" % ', '.join(ACCEPTED_EXTENSIONS)
            self.assertIn(error_message, upload_document_form.errors['file'])

    def test_allowed_extension(self):
        self.filename = 'executable_file.pdf'
        m = mock_open()
        with patch('__main__.open', m, create=True):
            with open(self.filename, 'w') as document:
                document.write("Some stuff")
            document = open(self.filename, 'rb')
            file_data = {'file': SimpleUploadedFile(self.filename, document.read())}
            upload_document_form = SupportDocumentUploadForm({}, file_data)
            self.assertTrue(upload_document_form.is_valid())