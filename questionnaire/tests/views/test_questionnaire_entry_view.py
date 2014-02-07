from django.test import Client
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, MultiChoiceAnswer, NumericalAnswer, QuestionGroupOrder, AnswerGroup
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryViewTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan")

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                     section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='B. Number of cases tested',
                                                 instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                                 UID='C00003', answer_type='Number')

        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                                 instructions="Include only those cases found positive for the infectious agent.",
                                                 UID='C00004', answer_type='Number')

        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group.question.add(self.question1, self.question3, self.question2)

        QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question1, order=1)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question2, order=2)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=self.question3, order=3)

        self.url = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id)

        self.client = Client()
        self.user = self.create_user_with_no_permissions()
        self.login_user()

        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'1', u'MultiChoice-TOTAL_FORMS': u'1',
                u'MultiChoice-INITIAL_FORMS': u'1', u'MultiChoice-0-response': self.option1.id,
                u'Number-INITIAL_FORMS': u'2', u'Number-TOTAL_FORMS': u'2', u'Number-MAX_NUM_FORMS': u'2',
                u'Number-0-response': u'2', u'Number-1-response': u'33'}


    def test_get_questionnaire_entry_view(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/index.html', templates)
        self.assertEqual(self.questionnaire, response.context['questionnaire'])
        self.assertEqual(self.section_1, response.context['section'])
        self.assertIsInstance(response.context['formsets'], QuestionnaireEntryFormService)

    def test_gets_ordered_sections_for_menu_breadcrumps_wizzard(self):
        section2 = Section.objects.create(title="section 2", order=2, questionnaire=self.questionnaire)
        section3 = Section.objects.create(title="section 3", order=3, questionnaire=self.questionnaire)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, response.context['ordered_sections'].count())
        self.assertEqual(self.section_1, response.context['ordered_sections'][0])
        self.assertEqual(section2, response.context['ordered_sections'][1])
        self.assertEqual(section3, response.context['ordered_sections'][2])

    def test_login_required(self):
        self.assert_login_required('/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id))


    def test_post_saves_answers(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/index.html', templates)

        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))

    def test_post_groups_rows_into_answer_groups(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)

        primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())
        answer_group_answers = answer_group[0].answer.all().select_subclasses()
        self.assertEqual(3, answer_group_answers.count())
        self.assertIn(primary, answer_group_answers)
        self.assertIn(answer_1, answer_group_answers)
        self.assertIn(answer_2, answer_group_answers)

    def test_successful_post_shows_success_message(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        expected_message = 'Draft saved.'
        self.assertIn(expected_message, response.content)


    def test_post_failure_does_not_save_answers(self):
        data = self.data
        data[u'MultiChoice-0-response'] = -1

        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        response = self.client.post(self.url, data=data)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/index.html', templates)

        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        self.failIf(AnswerGroup.objects.filter(grouped_question=self.question_group))

        expected_message = 'Draft NOT saved. See errors below.'
        self.assertIn(expected_message, response.content)

    def test_post_on_section_with_draft_answers_modify_original_draft_answers_and_not_create_new_instance(self):
        data = self.data
        self.client.post(self.url, data=data)

        old_primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1)
        old_answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2)
        old_answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3)

        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-1-response'] = '3'
        response = self.client.post(self.url, data=data_modified)
        self.assertEqual(200, response.status_code)

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']), question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']), question=self.question3)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(old_answer_2.id, answer_2.id)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())