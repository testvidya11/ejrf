from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.forms.questionnaire_entry import QuestionnaireEntryForm
from questionnaire.models import Questionnaire, Section, SubSection, QuestionGroup, Question
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



    def test_questionnaire_entry_form_formset_size_per_answer_type_should_match_number_of_question_per_answer_type(self):
        questionnaire_entry_form = QuestionnaireEntryForm(self.section1)
        formsets = questionnaire_entry_form._formsets()
        self.assertEqual(2, len(formsets['Number']))
        self.assertEqual(1, len(formsets['Text']))
        self.assertEqual(1, len(formsets['Date']))
        self.assertEqual(2, len(formsets['MultiChoice']))

    def test_questionnaire_entry_form_generates_all_answer_type_formsets(self):
        questionnaire_entry_form = QuestionnaireEntryForm(self.section1)
        formsets = questionnaire_entry_form._formsets()
        self.assertIsInstance(formsets['Number'][0], NumericalAnswerForm)
        self.assertIsInstance(formsets['Text'][0], TextAnswerForm)
        self.assertIsInstance(formsets['Date'][0], DateAnswerForm)
        self.assertIsInstance(formsets['MultiChoice'][0], MultiChoiceAnswerForm)
