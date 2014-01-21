from questionnaire.models import Section, SubSection
from questionnaire.models.questionnaires import Questionnaire
from questionnaire.tests.base_test import BaseTest


class QuestionnaireTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")
        self.sub_section_1 = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)
        self.sub_section_2 = SubSection.objects.create(title="Another", order=2, section=self.section_1)

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
        print type(questionnaire_sub_sections)
        self.assertEqual(2, len(questionnaire_sub_sections))
        self.assertIn(self.sub_section_1, questionnaire_sub_sections)
        self.assertIn(self.sub_section_2, questionnaire_sub_sections)