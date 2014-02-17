from django.test import Client
from questionnaire.forms.questions import QuestionForm
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

    def test_get_list_question(self):
        questions = Question.objects.create(text='B. Number of cases tested',
                                            instructions="Enter the total number of cases", UID='00001', answer_type='Number')

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/index.html', templates)
        self.assertIn(questions, response.context['questions'])

    def test_get_create_question(self):
        response = self.client.get(self.url + 'new/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questions/new.html', templates)
        self.assertIsNotNone(response.context['form'])
        self.assertEqual('CREATE', response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])

    def test_post_create_question(self):
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **self.form_data)
        response = self.client.post(self.url + 'new/', data=self.form_data)
        self.assertRedirects(response, self.url)
        self.failUnless(Question.objects.get(**self.form_data))
        self.assertIn("Question successfully created.", response.cookies['messages'].value)

    def test_post_create_with_invalid_form_returns_errors(self):
        form_data = self.form_data.copy()
        form_data['text'] = ''

        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        response = self.client.post(self.url + 'new/', data=form_data)
        self.assertRaises(Question.DoesNotExist, Question.objects.get, **form_data)
        self.assertIn('Question NOT created. See errors below.', response.content)
        self.assertIsInstance(response.context['form'], QuestionForm)
        self.assertEqual("CREATE", response.context['btn_label'])
        self.assertEqual("id-new-question-form", response.context['id'])