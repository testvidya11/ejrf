from questionnaire.models import Question, QuestionGroup, Questionnaire, SubSection, Section, Answer, Country, \
    Organization, Region, NumericalAnswer, QuestionOption, MultiChoiceAnswer, AnswerGroup
from questionnaire.services.export_data_service import ExportToTextService
from questionnaire.tests.base_test import BaseTest


class ExportToTextServiceTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan", year=2013)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                            instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                            UID='C00003', answer_type='Number')

        self.question2 = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00004', answer_type='Number')

        self.parent = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.parent.question.add(self.question1, self.question2)
        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro",organization=self.organisation)
        self.country = Country.objects.create(name="Uganda", code="UGX")
        self.regions.countries.add(self.country)

        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS,  response=23)
        self.question2_answer = NumericalAnswer.objects.create(question=self.question2, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=1)

    def test_exports_questions_with_numeric_answers(self):
        expected_data = [["2013\tUGX\t%s\t%s" % (self.question1.UID, '23.00')],
                         ["2013\tUGX\t%s\t%s" % (self.question2.UID, '1.00')]]

        export_to_text_service = ExportToTextService(self.questionnaire)
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)

    def test_exports_multichoice_answers_for_questionnaire(self):
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='MultiChoice')
        question1 = Question.objects.create(text='what do you drink at nite?', UID='abc125', answer_type='MultiChoice')
        self.parent.question.add(question, question1)
        country = Country.objects.create(name="Peru", code="PXR")
        option1 = QuestionOption.objects.create(text="Diphteria", question=question)
        QuestionOption.objects.create(text="Measles", question=question)
        option3 = QuestionOption.objects.create(text="Neonatal tetanus (NT)", question=question1)
        MultiChoiceAnswer.objects.create(question=question, country=country, response=option1,
                                         status=Answer.SUBMITTED_STATUS)
        MultiChoiceAnswer.objects.create(question=question1, country=country, response=option3,
                                         status=Answer.SUBMITTED_STATUS)

        MultiChoiceAnswer.objects.create(question=question1, country=country, response=option3,
                                         status=Answer.DRAFT_STATUS)

        expected_data = [["2013\tUGX\t%s\t%s" % (self.question1.UID, '23.00')],
                         ["2013\tUGX\t%s\t%s" % (self.question2.UID, '1.00')],
                         ["2013\tPXR\t%s\t%s" % (question.UID, option1.text)],
                         ["2013\tPXR\t%s\t%s" % (question1.UID, option3.text)]]

        export_to_text_service = ExportToTextService(self.questionnaire)
        actual_data = export_to_text_service.get_formatted_responses()
        self.assertEqual(len(expected_data), len(actual_data))
        self.assertIn(expected_data[0], actual_data)
        self.assertIn(expected_data[1], actual_data)