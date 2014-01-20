from questionnaire.models import Questionnaire, Section, SubSection, Question
from questionnaire.models.question_groups import QuestionGroup
from questionnaire.tests.base_test import BaseTest


class GroupedQuestionsTest(BaseTest):
    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="Immunisation Extra Coverage", order=1, section=self.section)

    def test_grouped_questions_field(self):
        grouped_question = QuestionGroup()
        fields = [str(item.attname) for item in grouped_question._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified','subsection_id', 'order']:
            self.assertIn(field, fields)

    def test_grouped_questions_store(self):
        grouped_question = QuestionGroup.objects.create(subsection=self.sub_section,  order=1)
        grouped_question.question.add(self.question)
        self.failUnless(grouped_question.id)
        self.assertEqual(1, grouped_question.order)
        self.assertEqual(self.sub_section, grouped_question.subsection)
        all_questions = grouped_question.question.all()
        self.assertEqual(1, all_questions.count())
        self.assertEqual(self.question, all_questions[0])