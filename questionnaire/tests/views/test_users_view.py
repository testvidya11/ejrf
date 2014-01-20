from django.contrib.auth.models import User
from django.test import Client
from questionnaire.tests.base_test import BaseTest


class UsersViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.general_user = User.objects.create_user(username='user', email='user@gmail.com')
        self.general_user.set_password('p622')
        self.general_user.save()
        self.client.login(username='user', password='p62')

    def test_get_login(self):
        response = self.client.get('/login/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('users/login.html', templates)