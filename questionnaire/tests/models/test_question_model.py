from django.test import TestCase
from questionnaire.models.questions import Question


class QuestionTest(TestCase):

    def test_question_fields(self):
        question = Question()
        fields = [str(item.attname) for item in question._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'instructions', 'UID', 'answer_type']:
            self.assertIn(field, fields)

    def test_question_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.failUnless(question.id)
        self.assertEqual('Uganda Revision 2014 what what?', question.text)
        self.assertIsNone(question.instructions)
        self.assertEqual('abc123', question.UID)