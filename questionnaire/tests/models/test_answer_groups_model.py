from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, Answer, Country
from questionnaire.models.answer_groups import AnswerGroup
from questionnaire.tests.base_test import BaseTest


class GroupedAnswerTest(BaseTest):
    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="Immunisation Extra Coverage", order=1, section=self.section)
        self.grouped_question = QuestionGroup.objects.create(subsection=self.sub_section)
        self.grouped_question.question.add(self.question)
        country = Country.objects.create(name="Peru")
        self.answer = Answer.objects.create(question=self.question, country=country)


    def test_grouped_answers_fields(self):
        group_answer = AnswerGroup()
        fields = [str(item.attname) for item in group_answer._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'answer_id', 'grouped_question_id', 'row']:
            self.assertIn(field, fields)

    def test_grouped_answers_store(self):
        grouped_answers = AnswerGroup.objects.create(answer=self.answer, grouped_question=self.grouped_question, row=1)
        self.failUnless(grouped_answers.id)
        self.assertEqual(1, grouped_answers.row)
        self.assertEqual(self.answer, grouped_answers.answer)
        self.assertEqual(self.grouped_question, grouped_answers.grouped_question)