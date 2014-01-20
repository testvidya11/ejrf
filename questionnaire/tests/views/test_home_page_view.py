from django.test import Client
from questionnaire.tests.base_test import BaseTest


class HomePageViewTest(BaseTest):

    def test_get(self):
        client = Client()
        response = client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)