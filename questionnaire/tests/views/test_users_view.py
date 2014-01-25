from django.contrib.auth.models import User
from django.test import Client
from questionnaire.forms.user_profile import UserProfileForm
from questionnaire.tests.base_test import BaseTest


class UsersViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user = self.create_user_with_no_permissions()
        self.login_user()
        self.form_data = {
            'username': 'rajni',
            'password1': 'kant',
            'password2': 'kant',
            'email': 'raj@ni.kant'}

    def test_get_login(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('users/login.html', templates)

    def test_get_list_users(self):
        user2 = User.objects.create(username='user1', email='rajni@kant.com')

        response = self.client.get('/users/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('users/index.html', templates)
        self.assertIn(self.user, response.context['users'])
        self.assertIn(user2, response.context['users'])

    def test_get_new(self):
        response = self.client.get('/users/new/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('users/new.html', templates)
        self.assertIsInstance(response.context['form'], UserProfileForm)
        self.assertIn('CREATE', response.context['btn_label'])
        self.assertIn('Create new user', response.context['title'])

    def test_post_new_user(self):
        response = self.client.post('/users/new/', data=self.form_data)
        self.assertRedirects(response, expected_url='/users/')
        user = User.objects.filter(username=self.form_data['username'])
        self.failUnless(user)
        self.assertIn('User created successfully.', response.cookies['messages'].value)