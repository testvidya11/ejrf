from django.test import Client
from questionnaire.forms.assign_question import AssignQuestionForm
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.tests.base_test import BaseTest


class QuestionnairePreviewTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.section = Section.objects.create(name="section", questionnaire=self.questionnaire, order=1)
        self.subsection = SubSection.objects.create(title="subsection 1", section=self.section, order=1)
        self.question1 = Question.objects.create(text='Q1', UID='C00003', answer_type='Number')
        self.question2 = Question.objects.create(text='Q2', UID='C00002', answer_type='Number')
        self.form_data = {'questions': [self.question1.id, self.question2.id]}
        self.url = '/subsection/%d/assign_questions/'%(self.subsection.id)

    def test_get_assign_question_page(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/assign_questions.html', templates)


    def test_gets_assign_questions_form_and_subsection_in_context(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['assign_question_form'], AssignQuestionForm)
        self.assertEqual(2, response.context['questions'].count())
        questions_texts = [question.text for question in list(response.context['questions'])]
        self.assertIn(self.question1.text, questions_texts)
        self.assertIn(self.question2.text, questions_texts)
        self.assertEqual('Done', response.context['btn_label'])

    def test_post_questions_assigns_them_to_subsections_and_get_or_create_group(self):
        self.failIf(self.question1.question_group.all())
        self.failIf(self.question2.question_group.all())

        response = self.client.post(self.url, {'questions':[self.question1.id, self.question2.id]})

        self.assertEqual(200, response.status_code)

        question_group = self.question1.question_group.all()
        self.assertEqual(1, question_group.count())
        self.assertEqual(question_group[0], self.question2.question_group.all()[0])
        self.assertEqual(self.subsection, question_group[0].subsection)

    def xtest_login_required(self):
        self.assert_login_required('/questionnaire/preview/')

    def xtest_permission_required(self):
        self.assert_permission_required('/questionnaire/preview/')
