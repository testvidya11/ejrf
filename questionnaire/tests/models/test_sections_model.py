from django.test import TestCase
from questionnaire.models.sections import Section
from questionnaire.models import Questionnaire


class SectionTest(TestCase):

    def test_section_fields(self):
        section = Section()
        fields = [str(item.attname) for item in section._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'questionnaire_id']:
            self.assertIn(field, fields)

    def test_questionnaire_store(self):
        questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=questionnaire)
        self.failUnless(section.id)
        self.assertEqual("Immunisation Coverage", section.title)
        self.assertEqual(questionnaire, section.questionnaire)