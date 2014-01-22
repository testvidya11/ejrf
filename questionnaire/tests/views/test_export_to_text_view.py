from django.test import Client
from questionnaire.models import Questionnaire
from questionnaire.tests.base_test import BaseTest


class ExportToTextViewTest(BaseTest):

    def test_get(self):
        client = Client()
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan", year=2013)
        response = client.get("/extract/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/extract.html', templates)
        self.assertIn(self.questionnaire, response.context['questionnaires'])