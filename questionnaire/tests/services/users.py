from django.contrib.auth.models import User
from questionnaire.models import Questionnaire, Section, SubSection, QuestionGroup, Question, QuestionGroupOrder, Country, QuestionOption, MultiChoiceAnswer, NumericalAnswer, AnswerGroup, UserProfile, Answer
from questionnaire.services.users import UserService
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryAsFormTest(BaseTest):

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

        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'1', u'MultiChoice-TOTAL_FORMS': u'1',
                u'MultiChoice-INITIAL_FORMS': u'1', u'MultiChoice-0-response': self.option1.id,
                u'Number-INITIAL_FORMS': u'2', u'Number-TOTAL_FORMS': u'2', u'Number-MAX_NUM_FORMS': u'2',
                u'Number-0-response': u'2', u'Number-1-response': u'33'}

        self.country = Country.objects.create(name="Uganda", code="UGA")
        self.user = User.objects.create(username="rajni")
        UserProfile.objects.create(user=self.user, country=self.country)

        self.initial = {'country': self.country, 'status': 'Draft', 'version':1, 'code': 'ABC123'}

    def test_user_knows_its_country_answers(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        user_service = UserService(self.user)
        user_answers = user_service.answers()

        self.assertEqual(3, len(user_answers))

        self.assertIn(old_primary, user_answers)
        self.assertIn(old_answer_1, user_answers)
        self.assertIn(old_answer_2, user_answers)

    def test_user_knows_answers_given_questionnaire(self):
        data = self.data
        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        other_questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                            description="From dropbox as given by Rouslan")
        other_section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1, questionnaire=other_questionnaire, name="Reported Cases")
        other_sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1,
                                                        section=other_section_1)
        other_question1 = Question.objects.create(text='Disease', UID='C00011', answer_type='Number')
        other_question_group = QuestionGroup.objects.create(subsection=other_sub_section, order=1)
        other_question_group.question.add(other_question1)
        other_answer_1 = NumericalAnswer.objects.create(response=1, question=other_question1)

        section_2 = Section.objects.create(title="Section 2", order=2, questionnaire=self.questionnaire, name="section2")
        sub_section2 = SubSection.objects.create(title="subsection 2", order=1, section=section_2)
        question1 = Question.objects.create(text='question 1', UID='C00013', answer_type='Number')
        question2 = Question.objects.create(text='question 2', UID='C00014', answer_type='Number')

        question_group = QuestionGroup.objects.create(subsection=sub_section2, order=1)
        question_group.question.add(question1, question2)

        QuestionGroupOrder.objects.create(question=question1, order=1, question_group=question_group)
        QuestionGroupOrder.objects.create(question=question2, order=2, question_group=question_group)

        answer_1 = NumericalAnswer.objects.create(response=1, question=question1, status=Answer.DRAFT_STATUS, country=self.country)
        answer_2 = NumericalAnswer.objects.create(response=2, question=question2, status=Answer.DRAFT_STATUS, country=self.country)

        answer_group = AnswerGroup.objects.create(grouped_question=question_group)
        answer_group.answer.add(answer_1, answer_2)

        user_service = UserService(self.user)
        user_answers = user_service.answers_in(self.questionnaire)

        self.assertEqual(5, len(user_answers))

        self.assertIn(old_primary, user_answers)
        self.assertIn(old_answer_1, user_answers)
        self.assertIn(old_answer_2, user_answers)
        self.assertNotIn(other_answer_1, user_answers)

        self.assertIn(answer_1, user_answers)
        self.assertIn(answer_2, user_answers)


    def test_submit_changes_draft_answers_to_submitted_and_not_create_new_instances(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        user_service = UserService(self.user)
        user_service.submit(self.questionnaire)

        primary = MultiChoiceAnswer.objects.get(response__id=int(data['MultiChoice-0-response']), question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data['Number-1-response']), question=self.question3)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(Answer.SUBMITTED_STATUS, primary.status)

        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(Answer.SUBMITTED_STATUS, answer_1.status)

        self.assertEqual(old_answer_2.id, answer_2.id)
        self.assertEqual(Answer.SUBMITTED_STATUS, answer_2.status)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())