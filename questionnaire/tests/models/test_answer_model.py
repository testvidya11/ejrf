from django.core.exceptions import ValidationError
from django.test import TestCase
from questionnaire.models import Question, Country
from questionnaire.models.answers import Answer, NumericalAnswer, TextAnswer


class AnswerTest(TestCase):

    def test_answer_fields(self):
        answer = Answer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(4, len(fields))
        for field in ['created', 'modified', 'question_id','country_id']:
            self.assertIn(field, fields)


class NumericalAnswerTest(TestCase):

    def test_numerical_answer_fields(self):
        answer = NumericalAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'question_id','country_id', 'response']:
            self.assertIn(field, fields)

    def test_numerical_answer_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        country = Country.objects.create(name="Peru")
        answer = NumericalAnswer.objects.create(question=question, country=country, response=11.2)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(11.2, answer.response)

    def test_numericalanswer_cannot_be_text(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        country = Country.objects.create(name="Peru")
        answer = NumericalAnswer(question=question, country=country, response='not a decimal number')
        self.assertRaises(ValidationError, answer.save)

class TextAnswerTest(TestCase):

    def test_text_answer_fields(self):
        answer = TextAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'question_id','country_id', 'response']:
            self.assertIn(field, fields)

    def test_text_answer_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        country = Country.objects.create(name="Peru")
        answer = TextAnswer.objects.create(question=question, country=country, response="this is a text repsonse")
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual("this is a text repsonse", answer.response)

