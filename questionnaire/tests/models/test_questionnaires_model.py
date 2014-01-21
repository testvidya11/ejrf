from questionnaire.models import Section, SubSection, Organization, Region, Country, NumericalAnswer, Answer, Question, QuestionGroup
from questionnaire.models.questionnaires import Questionnaire
from questionnaire.tests.base_test import BaseTest


class QuestionnaireTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")
        self.sub_section_1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)
        self.sub_section_2 = SubSection.objects.create(title="Another", order=2, section=self.section_1)
        self.organisation = Organization.objects.create(name="WHO")
        self.regions = Region.objects.create(name="The Afro",organization=self.organisation)
        self.country = Country.objects.create(name="Uganda")
        self.regions.countries.add(self.country)
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                            instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                            UID='C00003', answer_type='Number')
        self.sub_group = QuestionGroup.objects.create(subsection=self.sub_section_1, name="Laboratory Investigation")
        self.sub_group.question.add(self.question1)

        self.question1_answer = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS,  response=23)
        self.question1_answer_2 = NumericalAnswer.objects.create(question=self.question1, country=self.country,
                                                               status=Answer.SUBMITTED_STATUS, response=1)
    def test_questionnaire_fields(self):
        fields = [str(item.attname) for item in Questionnaire._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description']:
            self.assertIn(field, fields)

    def test_questionnaire_store(self):
        self.failUnless(self.questionnaire.id)
        self.assertEqual("JRF 2013 Core English", self.questionnaire.name)

    def test_questionnaire_can_find_its_subsection(self):
        questionnaire_sub_sections = self.questionnaire.sub_sections()
        self.assertEqual(2, len(questionnaire_sub_sections))
        self.assertIn(self.sub_section_1, questionnaire_sub_sections)
        self.assertIn(self.sub_section_2, questionnaire_sub_sections)

    def test_questionnaire_can_get_all_its_questions(self):
        all_questions = self.questionnaire.get_all_questions()
        self.assertEqual(1, len(all_questions))
        self.assertIn(self.question1, all_questions)