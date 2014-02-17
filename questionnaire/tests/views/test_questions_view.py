from django.test import Client
from questionnaire.models import Question
from questionnaire.tests.base_test import BaseTest


class SectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_view_users', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.url = '/questions/'
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'short_instruction': 'short version',
                          'answer_type': 'Number'}

    def test_get_create_section(self):
        questions = Question.objects.create(text='B. Number of cases tested',
                                            instructions="Enter the total number of cases", UID='00001', answer_type='Number')

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertIn(questions, response.context['questions'])