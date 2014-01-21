from django.test import TestCase
from questionnaire.models.sections import Section, SubSection
from questionnaire.models import Questionnaire, QuestionGroup, Question
from questionnaire.tests.base_test import BaseTest


class SectionBaseTest(BaseTest):
    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1,
                                              questionnaire=self.questionnaire, name="im cover" , description="section description")
        self.sub_section = SubSection.objects.create(title="Infant Immunisation Coverage", order=1, section=self.section)
        self.sub_section_1 = SubSection.objects.create(title="Infant Immunisation Coverage", order=2, section=self.section)

        self.question1 = Question.objects.create(text='Uganda Revision 2014 what what?', UID='ab3123', answer_type='Text')
        self.question2 = Question.objects.create(text='Uganda Revision 2014 what what?', UID='ab5123', answer_type='Text')

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


class SubSectionTest(SectionBaseTest):

    def test_sub_section_fields(self):
        sub_section = SubSection()
        fields = [str(item.attname) for item in sub_section._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'title', 'order', 'section_id', 'description']:
            self.assertIn(field, fields)

    def test_sub_section_store(self):
        self.failUnless(self.section.id)
        self.assertEqual("Infant Immunisation Coverage", self.sub_section.title)
        self.assertEqual(self.section, self.sub_section.section)

    def test_subsection_can_get_its_questions_groups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        self.assertEqual(1, len(self.sub_section.all_question_groups()))
        self.assertIn(sub_group, self.sub_section.all_question_groups())

    def test_subsection_can_get_its_questions_from_its_groups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        sub_group.question.add(self.question1, self.question2)

        questions = self.sub_section.all_questions()
        print questions
        self.assertEqual(2, len(questions))
        self.assertIn(self.question1, questions)
        self.assertIn(self.question2, questions)