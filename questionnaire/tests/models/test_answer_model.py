from django.test import TestCase
from questionnaire.models import Question, Region, Country
from questionnaire.models.answers import Answer, NumericalAnswer


class AnswerTest(TestCase):

    def test_answer_fields(self):
        answer = Answer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(4, len(fields))
        for field in ['created', 'modified', 'question_id','country_id']:
            self.assertIn(field, fields)


class NumericalAnswerTest(TestCase):

    def test_answer_fields(self):
        answer = NumericalAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'question_id','country_id', 'response']:
            self.assertIn(field, fields)

    def test_answer_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        country = Country.objects.create(name="Peru")
        answer = NumericalAnswer.objects.create(question=question, country=country, response=11.2)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(11.2, answer.response)