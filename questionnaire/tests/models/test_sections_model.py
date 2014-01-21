from django.test import TestCase
from questionnaire.models.sections import Section, SubSection
from questionnaire.models import Questionnaire
from questionnaire.tests.base_test import BaseTest


class SectionBaseTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1,
                                              questionnaire=self.questionnaire, name="im cover" , description="section description")
        self.sub_section = SubSection.objects.create(title="Infant Immunisation Coverage", order=1, section=self.section)
        self.sub_section_1 = SubSection.objects.create(title="Infant Immunisation Coverage", order=2, section=self.section)


class SectionTest(SectionBaseTest):

    def test_section_fields(self):
        section = Section()
        fields = [str(item.attname) for item in section._meta.fields]
        self.assertEqual(8, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'questionnaire_id', 'name', 'description']:
            self.assertIn(field, fields)

    def test_section_store(self):
        self.failUnless(self.section.id)
        self.assertEqual("Immunisation Coverage", self.section.title)
        self.assertEqual("im cover", self.section.name)
        self.assertEqual("section description", self.section.description)
        self.assertEqual(self.questionnaire, self.section.questionnaire)


    def test_gets_subsections(self):
        sub_sections = self.section.get_sub_sections()
        self.assertEqual(2, len(sub_sections))
        self.assertIn(self.sub_section_1, sub_sections)
        self.assertIn(self.sub_section, sub_sections)

class SubSectionTest(SectionBaseTest):

    def test_sub_section_fields(self):
        sub_section = SubSection()
        fields = [str(item.attname) for item in sub_section._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'section_id', 'description']:
            self.assertIn(field, fields)

    def test_sub_section_store(self):
        sub_section = SubSection.objects.create(title="Infant Immunisation Coverage", order=1, section=self.section)
        self.failUnless(self.section.id)
        self.assertEqual("Infant Immunisation Coverage", sub_section.title)
        self.assertEqual(self.section, sub_section.section)