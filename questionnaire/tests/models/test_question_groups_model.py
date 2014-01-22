from django.db import IntegrityError
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroupOrder
from questionnaire.models.question_groups import QuestionGroup
from questionnaire.tests.base_test import BaseTest


class GroupedQuestionsTest(BaseTest):
    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="Immunisation Extra Coverage", order=1, section=self.section)
        self.parent_question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.sub_grouped_question = QuestionGroup.objects.create(subsection=self.sub_section, parent=self.parent_question_group, order=2)
        self.sub_grouped_question.question.add(self.question)

    def test_grouped_questions_field(self):
        grouped_question = QuestionGroup()
        fields = [str(item.attname) for item in grouped_question._meta.fields]
        self.assertEqual(8, len(fields))
        for field in ['id', 'created', 'modified','subsection_id', 'name', 'instructions', 'parent_id', 'order']:
            self.assertIn(field, fields)

    def test_grouped_questions_store(self):
        grouped_question = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        grouped_question.question.add(self.question)
        self.failUnless(grouped_question.id)
        self.assertEqual(1, grouped_question.order)
        self.assertEqual(self.sub_section, grouped_question.subsection)
        all_questions = grouped_question.question.all()
        self.assertEqual(1, all_questions.count())
        self.assertEqual(self.question, all_questions[0])
        self.assertIsNone(grouped_question.name)
        self.assertIsNone(grouped_question.instructions)

    def test_grouped_questions_store_parent(self):
        self.assertEqual(self.parent_question_group, self.sub_grouped_question.parent)
        self.failUnless(self.sub_grouped_question.id)

    def test_grouped_question_can_get_its_questions(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='ab3123', answer_type='Text')
        sub_group.question.add(self.question, question)
        self.assertEqual(2, len(sub_group.all_questions()))
        self.assertIn(self.question, sub_group.all_questions())
        self.assertIn(question, sub_group.all_questions())

    def test_knows_its__subgroups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, parent=self.parent_question_group)
        sub_group2 = QuestionGroup.objects.create(subsection=self.sub_section, order=1, parent=self.parent_question_group)
        other_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)

        sub_groups = self.parent_question_group.sub_groups()

        self.assertEqual(3, len(sub_groups))
        self.assertIn(sub_group, sub_groups)
        self.assertIn(sub_group2, sub_groups)
        self.assertIn(self.sub_grouped_question, sub_groups)
        self.assertNotIn(other_group, sub_groups)

    def test_knows_all_questions_even_those_of_subgroups(self):
        sub_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1, parent=self.parent_question_group)
        question = Question.objects.create(text='question', UID='ab3123', answer_type='Text')
        question2 = Question.objects.create(text='question2', UID='c00001', answer_type='Text')
        sub_group.question.add(question, question2)

        QuestionGroupOrder.objects.create(question=self.question, question_group=self.parent_question_group, order=1)
        QuestionGroupOrder.objects.create(question=question, question_group=self.parent_question_group, order=2)
        QuestionGroupOrder.objects.create(question=question2, question_group=self.parent_question_group, order=3)

        known_questions = self.parent_question_group.and_sub_group_questions()

        self.assertEqual(3, len(known_questions))
        self.assertIn(self.question, known_questions)
        self.assertIn(question, known_questions)
        self.assertIn(question2, known_questions)

