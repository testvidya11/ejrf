from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.models import Questionnaire, Section, SubSection, QuestionGroup, Question, QuestionGroupOrder, NumericalAnswer, Answer, AnswerGroup, Country, TextAnswer, QuestionOption, MultiChoiceAnswer, DateAnswer
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryAsServiceTest(BaseTest):

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
        self.initial = {'status': 'Draft', 'country': self.country}

    def test_questionnaire_entry_form_formset_size_per_answer_type_should_match_number_of_question_per_answer_type(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()
        self.assertEqual(2, len(formsets['Number']))
        self.assertEqual(1, len(formsets['Text']))
        self.assertEqual(1, len(formsets['Date']))
        self.assertEqual(2, len(formsets['MultiChoice']))

    def test_questionnaire_entry_form_generates_all_answer_type_formsets(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()
        self.assertIsInstance(formsets['Number'][0], NumericalAnswerForm)
        self.assertIsInstance(formsets['Text'][0], TextAnswerForm)
        self.assertIsInstance(formsets['Date'][0], DateAnswerForm)
        self.assertIsInstance(formsets['MultiChoice'][0], MultiChoiceAnswerForm)

    def test_should_order_forms(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question1, formsets['MultiChoice'][0].initial['question'])
        self.assertEqual(self.question2, formsets['Text'][0].initial['question'])
        self.assertEqual(self.question3, formsets['Number'][0].initial['question'])
        self.assertEqual(self.question4, formsets['MultiChoice'][1].initial['question'])
        self.assertEqual(self.question5, formsets['Number'][1].initial['question'])
        self.assertEqual(self.question6, formsets['Date'][0].initial['question'])

    def test_should_give_correct_form_for_question(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)

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
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(self.question_group, formsets['MultiChoice'][0].initial['group'])
        self.assertEqual(self.question_group, formsets['Text'][0].initial['group'])
        self.assertEqual(self.question_group, formsets['Number'][0].initial['group'])
        self.assertEqual(self.question_group2, formsets['MultiChoice'][1].initial['group'])
        self.assertEqual(self.question_group2, formsets['Number'][1].initial['group'])
        self.assertEqual(self.question_group3, formsets['Date'][0].initial['group'])

    def test_initial_gets_response_if_there_is_draft_answer_for_country(self):
        question2_answer = TextAnswer.objects.create(question=self.question2, country=self.country,
                                                               status=Answer.DRAFT_STATUS, response="ayoyoyo")
        question3_answer = NumericalAnswer.objects.create(question=self.question3, country=self.country,
                                                               status=Answer.DRAFT_STATUS, response=1)
        answer_group1 = AnswerGroup.objects.create(grouped_question=self.question_group, row=1)
        answer_group1.answer.add(question2_answer, question3_answer)

        country_2 = Country.objects.create(name="Uganda 2")
        question1_answer_2 = NumericalAnswer.objects.create(question=self.question1, country=country_2,
                                                          status=Answer.DRAFT_STATUS, response=23)
        question2_answer_2 = NumericalAnswer.objects.create(question=self.question2, country=country_2,
                                                          status=Answer.DRAFT_STATUS, response=1)
        answer_group_2 = AnswerGroup.objects.create(grouped_question=self.question_group, row=2)
        answer_group_2.answer.add(question1_answer_2, question2_answer_2)

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
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

        self.country = Country.objects.create(name="Uganda")

        self.initial = {'country': self.country, 'status': 'Draft', 'version':1, 'code': 'ABC123'}

    def test_section_form_is_valid_if_all_form_in_all_formsets_are_valid(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=self.data)

        self.assertTrue(questionnaire_entry_form.is_valid())

    def test_section_form_is_invalid_if_any_form_in_any_formsets_are_invalid(self):
        invalid_data = self.data.copy()
        invalid_data[u'MultiChoice-0-response'] = -1

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=invalid_data)

        question1_form = questionnaire_entry_form.next_ordered_form(self.question1)

        self.assertFalse(questionnaire_entry_form.is_valid())
        error_message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([error_message], question1_form.errors['response'])

    def test_save_create_answer_objects(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=data)
        questionnaire_entry_form.save()

        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question2))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))

    def test_save_groups_rows_into_answer_groups(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))
        self.failIf(AnswerGroup.objects.filter(grouped_question=self.question_group))

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=data)
        questionnaire_entry_form.save()

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

    def test_save_on_already_existing_draft_answers_modify_original_draft_answers_and_not_create_new_instance(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-1-response'] = '3'

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=data_modified)
        questionnaire_entry_form.is_valid()
        questionnaire_entry_form.save()

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']), question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']), question=self.question3)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(old_answer_2.id, answer_2.id)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

    def test_submit_changes_draft_answers_to_submitted_and_not_create_new_instances(self):
        data = self.data

        old_primary = MultiChoiceAnswer.objects.create(response=self.option1, question=self.question1, **self.initial)
        old_answer_1 = NumericalAnswer.objects.create(response=int(data['Number-0-response']), question=self.question2, **self.initial)
        old_answer_2 = NumericalAnswer.objects.create(response=int(data['Number-1-response']), question=self.question3, **self.initial)

        answer_group = AnswerGroup.objects.create(grouped_question=self.question_group)
        answer_group.answer.add(old_primary, old_answer_1, old_answer_2)

        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-1-response'] = '3'

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=data_modified)
        questionnaire_entry_form.save()

        primary = MultiChoiceAnswer.objects.get(response__id=int(data_modified['MultiChoice-0-response']), question=self.question1)
        answer_1 = NumericalAnswer.objects.get(response=int(data_modified['Number-0-response']), question=self.question2)
        answer_2 = NumericalAnswer.objects.get(response=int(data_modified['Number-1-response']), question=self.question3)

        self.assertEqual(old_primary.id, primary.id)
        self.assertEqual(old_answer_1.id, answer_1.id)
        self.assertEqual(old_answer_2.id, answer_2.id)

        answer_group = AnswerGroup.objects.filter(grouped_question=self.question_group)
        self.assertEqual(1, answer_group.count())

    def test_integer_casting_of_numeric_responses(self):
        question5 = Question.objects.create(text='C. Number of cases positive', UID='C00333', answer_type='Text')
        self.question_group.question.add(question5)
        QuestionGroupOrder.objects.create(question_group=self.question_group, question=question5, order=4)
        self.data.update({u'Text-MAX_NUM_FORMS': u'1', u'Text-TOTAL_FORMS': u'1', u'Text-INITIAL_FORMS': u'1'})

        data = self.data
        data_modified = data.copy()
        data_modified['MultiChoice-0-response'] = self.option2.id
        data_modified['Number-0-response'] = 3.0
        data_modified['Number-1-response'] = 3.05
        data_modified['Text-0-response'] = 'haha'

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section_1, initial=self.initial, data=data_modified)
        questionnaire_entry_form.save()

        question1_form = questionnaire_entry_form.next_ordered_form(self.question1)
        question2_form = questionnaire_entry_form.next_ordered_form(self.question2)
        question3_form = questionnaire_entry_form.next_ordered_form(self.question3)
        question5_form = questionnaire_entry_form.next_ordered_form(question5)

        self.assertEqual(self.option2.id,  question1_form['response'].value())
        self.assertEqual(3, question2_form['response'].value())
        self.assertEqual(3.05, question3_form['response'].value())
        self.assertEqual("haha", question5_form['response'].value())


class GridQuestionGroupEntryServiceTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English")

        self.section1 = Section.objects.create(title="Reported Cases of Selected Vaccine", order=1,
                                               questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="subsection 1", order=1, section=self.section1)
        self.sub_section2 = SubSection.objects.create(title="subsection 2", order=2, section=self.section1)

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, grid=True, display_all=True)

        self.question1 = Question.objects.create(text='Favorite beer 1', UID='C00001', answer_type='MultiChoice', is_primary=True)
        self.option1 = QuestionOption.objects.create(text='tusker lager', question=self.question1)
        self.option2 = QuestionOption.objects.create(text='tusker lager1', question=self.question1)
        self.option3 = QuestionOption.objects.create(text='tusker lager2', question=self.question1)

        self.question2 = Question.objects.create(text='question 2', instructions="instruction 2",
                                                 UID='C00002', answer_type='Text')

        self.question3 = Question.objects.create(text='question 3', instructions="instruction 3",
                                                 UID='C00003', answer_type='Number')

        self.question4 = Question.objects.create(text='question 4', instructions="instruction 2",
                                                 UID='C00005', answer_type='Date')
        self.question_group.question.add(self.question1, self.question3, self.question2, self.question4)

        QuestionGroupOrder.objects.create(question=self.question1, question_group=self.question_group, order=1)
        QuestionGroupOrder.objects.create(question=self.question2, question_group=self.question_group, order=2)
        QuestionGroupOrder.objects.create(question=self.question3, question_group=self.question_group, order=3)
        QuestionGroupOrder.objects.create(question=self.question4, question_group=self.question_group, order=4)
        self.country = Country.objects.create(name="Uganda")
        self.initial = {'country': self.country, 'status': 'Draft', 'version': 1, 'code': 'ABC123'}
        self.data = {u'MultiChoice-MAX_NUM_FORMS': u'3', u'MultiChoice-TOTAL_FORMS': u'3',
                     u'MultiChoice-INITIAL_FORMS': u'3', u'MultiChoice-0-response': self.option1.id,
                     u'MultiChoice-1-response': self.option2.id,  u'MultiChoice-2-response': self.option3.id,
                     u'Number-MAX_NUM_FORMS': u'3', u'Number-TOTAL_FORMS': u'3',
                     u'Number-INITIAL_FORMS': u'3', u'Number-0-response': '22',
                     u'Number-1-response': '44',  u'Number-2-response': '33',
                     u'Text-MAX_NUM_FORMS': u'3', u'Text-TOTAL_FORMS': u'3',
                     u'Text-INITIAL_FORMS': u'3', u'Text-0-response': 'Haha',
                     u'Text-1-response': 'Hehe',  u'Text-2-response': 'hehehe',
                     u'Date-MAX_NUM_FORMS': u'3', u'Date-TOTAL_FORMS': u'3',
                     u'Date-INITIAL_FORMS': u'3', u'Date-0-response': '2014-2-2',
                     u'Date-1-response': '2014-2-2',  u'Date-2-response': '2014-2-2',
                     }

    def test_returns_multiple_forms_in_formsets_for_all_questions(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(3, len(formsets['Number']))
        self.assertEqual(3, len(formsets['Text']))
        self.assertEqual(3, len(formsets['Date']))
        self.assertEqual(3, len(formsets['MultiChoice']))

    def test_returns_multichoice_question_initial_for_all_question_options(self):
        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()
        self.assertEqual(self.option1, formsets['MultiChoice'][0].initial['response'])

        formset_ = questionnaire_entry_form.next_ordered_form(self.question1)
        self.assertEqual(self.option1, formset_.initial['response'])

        formset_ = questionnaire_entry_form.next_ordered_form(self.question1)
        self.assertEqual(self.option2, formset_.initial['response'])

        formset_ = questionnaire_entry_form.next_ordered_form(self.question1)
        self.assertEqual(self.option3, formset_.initial['response'])

    def test_returns_save_grid_with_display_all(self):
        data = self.data
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response'])))
        self.failIf(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-1-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-0-response'])))
        self.failIf(NumericalAnswer.objects.filter(response=int(data['Number-1-response'])))

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial, data=data)
        questionnaire_entry_form.is_valid()
        questionnaire_entry_form.save()

        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-0-response']), question=self.question1))
        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-1-response']), question=self.question1))
        self.failUnless(MultiChoiceAnswer.objects.filter(response__id=int(data['MultiChoice-2-response']), question=self.question1))

        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-0-response']), question=self.question3))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-1-response']), question=self.question3))
        self.failUnless(NumericalAnswer.objects.filter(response=int(data['Number-2-response']), question=self.question3))

        self.failUnless(TextAnswer.objects.filter(response=data['Text-0-response'], question=self.question2))
        self.failUnless(TextAnswer.objects.filter(response=data['Text-1-response'], question=self.question2))
        self.failUnless(TextAnswer.objects.filter(response=data['Text-2-response'], question=self.question2))

        self.failUnless(DateAnswer.objects.filter(response=data['Date-0-response'], question=self.question4))
        self.failUnless(DateAnswer.objects.filter(response=data['Date-1-response'], question=self.question4))
        self.failUnless(DateAnswer.objects.filter(response=data['Date-2-response'], question=self.question4))

    def test_returns_multiple_forms_in_formsets_for_all_questions_given_several_groups(self):
        question = Question.objects.create(text='Favorite beer 1', UID='C00033', answer_type='MultiChoice')
        yes = QuestionOption.objects.create(text='Yes', question=question)
        no = QuestionOption.objects.create(text='No', question=question)

        question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=2)
        question_group.question.add(question)
        QuestionGroupOrder.objects.create(question=question, question_group=question_group, order=1)

        questionnaire_entry_form = QuestionnaireEntryFormService(self.section1, initial=self.initial)
        formsets = questionnaire_entry_form._formsets()

        self.assertEqual(3, len(formsets['Number']))
        self.assertEqual(3, len(formsets['Text']))
        self.assertEqual(3, len(formsets['Date']))
        self.assertEqual(4, len(formsets['MultiChoice']))