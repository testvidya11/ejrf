from django.forms.formsets import formset_factory
from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionGroupOrder
from questionnaire.services.question_answer_form_ordering import QuestionAnswerFormOrdering
from questionnaire.tests.base_test import BaseTest


class QuestionAnswerFormOrderingServiceTest(BaseTest):

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


        numeric_formset_factory = formset_factory(NumericalAnswerForm, extra=2)
        text_formset_factory = formset_factory(TextAnswerForm)
        date_formset_factory = formset_factory(DateAnswerForm)
        multichoice_formset_factory = formset_factory(MultiChoiceAnswerForm, extra=2)

        self.numeric_form_set = numeric_formset_factory()
        self.text_form_set = text_formset_factory()
        self.date_form_set = date_formset_factory()
        self.multichoice_form_set = multichoice_formset_factory()

        self.formset={'Number': self.numeric_form_set,
                 'Text': self.text_form_set,
                 'Date': self.date_form_set,
                 'MultiChoice': self.multichoice_form_set,}


    def test_should_order_questions(self):
        question_answer_ordering = QuestionAnswerFormOrdering(self.section1, self.formset)
        questions = question_answer_ordering.get_ordered_questions()
        self.assertEqual(6, len(questions))
        self.assertEqual(self.question1, questions[0])
        self.assertEqual(self.question2, questions[1])
        self.assertEqual(self.question3, questions[2])
        self.assertEqual(self.question4, questions[3])
        self.assertEqual(self.question5, questions[4])
        self.assertEqual(self.question6, questions[5])

    def test_should_order_forms(self):
        question_answer_ordering = QuestionAnswerFormOrdering(self.section1, self.formset)
        ordered_forms = question_answer_ordering.ordered_forms()
        self.assertEqual(6, len(ordered_forms.keys()))
        self.assertIsInstance(ordered_forms[self.question1], MultiChoiceAnswerForm)
        self.assertIsInstance(ordered_forms[self.question2], TextAnswerForm)
        self.assertIsInstance(ordered_forms[self.question3], NumericalAnswerForm)
        self.assertIsInstance(ordered_forms[self.question4], MultiChoiceAnswerForm)
        self.assertIsInstance(ordered_forms[self.question5], NumericalAnswerForm)
        self.assertIsInstance(ordered_forms[self.question6], DateAnswerForm)

        self.assertEqual(self.question1, ordered_forms[self.question1].initial['question'])
        self.assertEqual(self.question2, ordered_forms[self.question2].initial['question'])
        self.assertEqual(self.question3, ordered_forms[self.question3].initial['question'])
        self.assertEqual(self.question4, ordered_forms[self.question4].initial['question'])
        self.assertEqual(self.question5, ordered_forms[self.question5].initial['question'])
        self.assertEqual(self.question6, ordered_forms[self.question6].initial['question'])
