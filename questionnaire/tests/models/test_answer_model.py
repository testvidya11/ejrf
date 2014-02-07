from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase
from questionnaire.models import Question, Country, QuestionOption, MultiChoiceAnswer
from questionnaire.models.answers import Answer, NumericalAnswer, TextAnswer, DateAnswer


class AnswerTest(TestCase):

    def test_answer_fields(self):
        answer = Answer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(8, len(fields))
        for field in ['id', 'created', 'modified', 'status', 'version', 'question_id', 'country_id', 'code']:
            self.assertIn(field, fields)

    def test_answer_stores(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Number')
        country = Country.objects.create(name="Peru")
        answer = Answer.objects.create(question=question, country=country)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(None, answer.code)


class NumericalAnswerTest(TestCase):

    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Date')
        self.country = Country.objects.create(name="Peru")

    def test_numerical_answer_fields(self):
        answer = NumericalAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(10, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response', 'code']:
            self.assertIn(field, fields)

    def test_numerical_answer_store(self):
        answer = NumericalAnswer.objects.create(question=self.question, country=self.country, response=11.2)
        self.failUnless(answer.id)
        self.assertEqual(self.question, answer.question)
        self.assertEqual(self.country, answer.country)
        self.assertEqual(11.2, answer.response)

    def test_numerical_answer_cannot_be_text(self):
        answer = NumericalAnswer(question=self.question, country=self.country, response='not a decimal number')
        self.assertRaises(ValidationError, answer.save)


class TextAnswerTest(TestCase):

    def test_text_answer_fields(self):
        answer = TextAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(10, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response', 'code']:
            self.assertIn(field, fields)

    def test_text_answer_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        country = Country.objects.create(name="Peru")
        answer = TextAnswer.objects.create(question=question, country=country, response="this is a text repsonse")
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual("this is a text repsonse", answer.response)


class DateAnswerTest(TestCase):

    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Date')
        self.country = Country.objects.create(name="Peru")

    def test_date_answer_fields(self):
        answer = DateAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(10, len(fields))
        for field in ['id', 'created', 'modified', 'question_id','country_id', 'response', 'code']:
            self.assertIn(field, fields)

    def test_date_answer_store(self):
        some_date = date.today()
        answer = DateAnswer.objects.create(question=self.question, country=self.country, response=some_date)
        self.failUnless(answer.id)
        self.assertEqual(self.question, answer.question)
        self.assertEqual(self.country, answer.country)
        self.assertEqual(some_date, answer.response)

    def test_date_answer_can_only_be_date(self):
        not_date = 'hahaha'
        answer = DateAnswer(question=self.question, country=self.country, response=not_date)
        self.assertRaises(ValidationError, answer.save)


class MultiChoiceAnswerTest(TestCase):

    def test_mulitchoice_answer_fields(self):
        answer = MultiChoiceAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(10, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response_id', 'code']:
            self.assertIn(field, fields)

    def test_mulitchoice_answer_store(self):
        question = Question.objects.create(text='what do you drink?', UID='abc123', answer_type='MultiChoice')
        country = Country.objects.create(name="Peru")
        option = QuestionOption.objects.create(text="whisky", question=question)
        some_date = date.today()
        answer = MultiChoiceAnswer.objects.create(question=question, country=country, response=option)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(option, answer.response)