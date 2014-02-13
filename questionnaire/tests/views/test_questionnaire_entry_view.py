from django.test import Client
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, MultiChoiceAnswer, NumericalAnswer, QuestionGroupOrder, AnswerGroup, Answer
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
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

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
        self.assertEqual(False, response.context['printable'])

    def test_gets_printable_as_true_if_set_in_request(self):
        url = '/questionnaire/entry/%d/section/%d/?printable=true' % (self.questionnaire.id, self.section_1.id)
        response = self.client.get(url)
        self.assertEqual(True, response.context['printable'])

    def test_login_required(self):
        self.assert_login_required('/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id))

    def test_permission_required(self):
        self.assert_permission_required('/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id))

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

    def test_post_failure_does_not_save_answers_and_does_not_redirect(self):
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

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']), question=self.question1, version=0)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']), question=self.question2, version=0)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']), question=self.question3, version=0)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(old_answer_2.id, answer_2.id)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

    def test_post_submit_save_draft_and_changes_all_answers_statuses_to_submitted(self):
        other_section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                 order=2, questionnaire=self.questionnaire, name="Reported Cases")
        other_sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                      section=other_section_1)
        other_question1 = Question.objects.create(text='other question 1', UID='C00011', answer_type='Number')
        other_question2 = Question.objects.create(text='other question 2', UID='C00012', answer_type='Number')

        other_question_group = QuestionGroup.objects.create(subsection=other_sub_section, order=1)
        other_question_group.question.add(other_question1, other_question2)

        QuestionGroupOrder.objects.create(question=other_question1, order=1, question_group=other_question_group)
        QuestionGroupOrder.objects.create(question=other_question2, order=2, question_group=other_question_group)

        other_answer_1 = NumericalAnswer.objects.create(response=1, question=other_question1, status=Answer.DRAFT_STATUS, country=self.country, version=0)
        other_answer_2 = NumericalAnswer.objects.create(response=2, question=other_question2, status=Answer.DRAFT_STATUS, country=self.country, version=0)

        answer_group = AnswerGroup.objects.create(grouped_question=other_question_group)
        answer_group.answer.add(other_answer_1, other_answer_2)

        data = self.data
        data['final_submit'] = True
        self.client.post(self.url, data=data)

        old_primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1, version=0)
        old_answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2, version=0)
        old_answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3, version=0)

        self.assertEqual(Answer.SUBMITTED_STATUS, old_primary.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, old_answer_1.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, old_answer_2.status)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

        other_answer_1 = NumericalAnswer.objects.get(response=1, question=other_question1, country=self.country, version=0)
        other_answer_2 = NumericalAnswer.objects.get(response=2, question=other_question2, country=self.country, version=0)

        self.assertEqual(Answer.SUBMITTED_STATUS, other_answer_1.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, other_answer_2.status)

        answer_group = AnswerGroup.objects.filter(grouped_question=other_question_group)
        self.assertEqual(1, answer_group.count())

    def test_post_after_submit_save_new_draft_version(self):
        data = self.data.copy()
        data['final_submit'] = True
        self.client.post(self.url, data=data)

        old_primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1, version=0)
        old_answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2, version=0)
        old_answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3, version=0)

        self.assertEqual(Answer.SUBMITTED_STATUS, old_primary.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, old_answer_1.status)
        self.assertEqual(Answer.SUBMITTED_STATUS, old_answer_2.status)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

        data = self.data
        self.client.post(self.url, data=data)

        primary = MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1, version=1)
        answer_1 = NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2, version=1)
        answer_2 = NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3, version=1)

        self.assertEqual(1, primary.count())
        self.assertEqual(Answer.DRAFT_STATUS, primary[0].status)
        self.assertEqual(1, primary[0].version)

        self.assertEqual(1, answer_1.count())
        self.assertEqual(Answer.DRAFT_STATUS, answer_1[0].status)
        self.assertEqual(1, answer_1[0].version)

        self.assertEqual(1, answer_2.count())
        self.assertEqual(Answer.DRAFT_STATUS, answer_2[0].status)
        self.assertEqual(1, answer_2[0].version)

    def test_post_saves_answers_and_redirect_if_given_redirect_url(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        section_2 = Section.objects.create(name="haha", questionnaire=self.questionnaire, order=2)
        data['redirect_url'] = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, section_2.id)

        response = self.client.post(self.url, data=data)

        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))

        self.assertRedirects(response, data['redirect_url'])

    def test_post_submit_answers_and_redirect_with_error_message_when_form_is_invalid(self):
        data = self.data.copy()
        data['final_submit'] = True
        data['MultiChoice-0-response'] = 'Stuff'
        section_2 = Section.objects.create(name="haha", questionnaire=self.questionnaire, order=2)
        data['redirect_url'] = '/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, section_2.id)

        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))

        message = 'Submission NOT completed. See errors below.'
        response = self.client.post(self.url, data=data)
        self.assertIn(message, response.content)
