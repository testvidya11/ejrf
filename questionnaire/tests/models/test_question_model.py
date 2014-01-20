from django.db import IntegrityError
from questionnaire.models.questions import Question, QuestionOption
from questionnaire.tests.base_test import BaseTest


class QuestionTest(BaseTest):

    def test_question_fields(self):
        question = Question()
        fields = [str(item.attname) for item in question._meta.fields]
        self.assertEqual(8, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'instructions', 'UID', 'answer_type', 'short_instruction']:
            self.assertIn(field, fields)

    def test_question_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.failUnless(question.id)
        self.assertEqual('Uganda Revision 2014 what what?', question.text)
        self.assertIsNone(question.instructions)
        self.assertIsNone(question.short_instruction)
        self.assertEqual('abc123', question.UID)

    def test_question_uid_is_unique(self):
        a_question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        question_with_same_uid = Question(text='haha', UID='abc123', answer_type='Text')
        self.assertRaises(IntegrityError, question_with_same_uid.save)


class QuestionOptionTest(BaseTest):

    def test_question_option_fields(self):
        question = QuestionOption()
        fields = [str(item.attname) for item in question._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'question_id']:
            self.assertIn(field, fields)

    def test_question_store(self):
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='Text')
        question_option = QuestionOption.objects.create(text='tusker lager', question=question)

        self.failUnless(question_option.id)
        self.assertEqual('tusker lager', question_option.text)
        self.assertEqual(question, question_option.question)