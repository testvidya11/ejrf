from urllib import quote
from django.contrib.auth.models import User
from django.test import Client
from questionnaire.tests.base_test import BaseTest


class HomePageViewTest(BaseTest):
    def setUp(self):
        self.user = User.objects.create(username="user", email="user@mail.com")
        self.user.set_password("pass")
        self.user.save()
        self.client = Client()
        self.client.login(username='user', password='pass')

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)

    def test_login_required_for_home_get(self):
        self.client.logout()
        response = self.client.get("/")
        self.assertRedirects(response, expected_url='accounts/login/?next=%s' % quote('/'), status_code=302)