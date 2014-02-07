from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section, SubSection, QuestionGroup, Question, QuestionGroupOrder, NumericalAnswer, Answer, AnswerGroup, Country, TextAnswer
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group2 = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        self.question_group3 = QuestionGroup.objects.create(subsection=self.sub_section2, order=1)

        self.question1 = Question.objects.create(text='question 1', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                    UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                            UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4', UID='C00004', answer_type='MultiChoice')
        self.question5 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                    UID='C00005', answer_type='Number')


        self.question6 = Question.objects.create(text='question 6', instructions="instruction 3",
                                            UID='C00006', answer_type='Date')

        self.question_group.question.add(self.question1, self.question3, self.question2)
        self.question_group2.question.add(self.question4, self.question5)
        self.question_group3.question.add(self.question6)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.question_group, order=2)
        QuestionGroupOrder.objects.create(question=self.question3, question_group=self.question_group, order=3)
        QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group2, order=1)
        QuestionGroupOrder.objects.create(question=self.question5, question_group=self.question_group2, order=2)
        QuestionGroupOrder.objects.create(question=self.question6, question_group=self.question_group3, order=1)

        self.country = Country.objects.create(name="Uganda")

    def test_questionnaire_entry_form_formset_size_per_answer_type_should_match_number_of_question_per_answer_type(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1)
        formsets = questionnaire_entry_form._formsets()
        self.assertEqual(2, len(formsets['Number']))
        self.assertEqual(1, len(formsets['Text']))
        self.assertEqual(1, len(formsets['Date']))
        self.assertEqual(2, len(formsets['MultiChoice']))

    def test_questionnaire_entry_form_generates_all_answer_type_formsets(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1)
        formsets = questionnaire_entry_form._formsets()
        self.assertIsInstance(formsets['Number'][0], NumericalAnswerForm)
        self.assertIsInstance(formsets['Text'][0], TextAnswerForm)
        self.assertIsInstance(formsets['Date'][0], DateAnswerForm)
        self.assertIsInstance(formsets['MultiChoice'][0], MultiChoiceAnswerForm)

    def test_should_order_forms(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question4, formsets['MultiChoice'][1].initial['question'])
        self.assertEqual(self.question5, formsets['Number'][1].initial['question'])
        self.assertEqual(self.question6, formsets['Date'][0].initial['question'])

    def test_should_give_correct_form_for_question(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1)

        question_form = questionnaire_entry_form.next_ordered_form(self.question1)
        self.assertIsInstance(question_form, MultiChoiceAnswerForm)
        self.assertEqual(self.question1, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question2)
        self.assertIsInstance(question_form, TextAnswerForm)
        self.assertEqual(self.question2, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question3)
        self.assertIsInstance(question_form, NumericalAnswerForm)
        self.assertEqual(self.question3, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question4)
        self.assertIsInstance(question_form, MultiChoiceAnswerForm)
        self.assertEqual(self.question4, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question5)
        self.assertIsInstance(question_form, NumericalAnswerForm)
        self.assertEqual(self.question5, question_form.initial['question'])

        question_form = questionnaire_entry_form.next_ordered_form(self.question6)
        self.assertIsInstance(question_form, DateAnswerForm)
        self.assertEqual(self.question6, question_form.initial['question'])

    def test_should_append_groups_in_initial(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question_group, formsets['MultiChoice'][0].initial['group'])
        self.assertEqual(self.question_group, formsets['Text'][0].initial['group'])
        self.assertEqual(self.question_group, formsets['Number'][0].initial['group'])
        self.assertEqual(self.question_group2, formsets['MultiChoice'][1].initial['group'])
        self.assertEqual(self.question_group2, formsets['Number'][1].initial['group'])
        self.assertEqual(self.question_group3, formsets['Date'][0].initial['group'])

    def test_initial_gets_response_if_there_is_draft_answer(self):
        question2_answer = TextAnswer.objects.create(question=self.question2, country=self.country,
                                                               status=Answer.DRAFT_STATUS, response="ayoyoyo")
        question3_answer = NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                               status=Answer.DRAFT_STATUS, response=1)
        answer_group1 = AnswerGroup.objects.create(grouped_question=self.question_group, row=1)
        answer_group1.answer.add(question2_answer, question3_answer)

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question4, formsets['MultiChoice'][1].initial['question'])
        self.assertEqual(self.question5, formsets['Number'][1].initial['question'])
        self.assertEqual(self.question6, formsets['Date'][0].initial['question'])


        self.assertNotIn('response', formsets['MultiChoice'][0].initial.keys())
        self.assertEqual(question2_answer.response, formsets['Text'][0].initial['response'])
        self.assertEqual(question3_answer.response, formsets['Number'][0].initial['response'])
        self.assertNotIn('response', formsets['MultiChoice'][1].initial.keys())
        self.assertNotIn('response', formsets['Number'][1].initial.keys())
        self.assertNotIn('response', formsets['Date'][0].initial.keys())

        self.assertNotIn('answer', formsets['MultiChoice'][0].initial.keys())
        self.assertEqual(question2_answer, formsets['Text'][0].initial['answer'])
        self.assertEqual(question3_answer, formsets['Number'][0].initial['answer'])
        self.assertNotIn('answer', formsets['MultiChoice'][1].initial.keys())
        self.assertNotIn('answer', formsets['Number'][1].initial.keys())
        self.assertNotIn('answer', formsets['Date'][0].initial.keys())
