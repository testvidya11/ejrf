from urllib import quote
from django.test import Client
from questionnaire.tests.base_test import BaseTest


class HomePageViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user = self.create_user_with_no_permissions()
        self.login_user()

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)

    def test_login_required_for_home_get(self):
        self.client.logout()
        response = self.client.get("/")
        self.assertRedirects(response, expected_url='accounts/login/?next=%s' % quote('/'), status_code=302)