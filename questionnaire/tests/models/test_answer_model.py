from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase
from questionnaire.models import Question, Country, QuestionOption, MultiChoiceAnswer
from questionnaire.models.answers import Answer, NumericalAnswer, TextAnswer, DateAnswer


class AnswerTest(TestCase):

    def test_answer_fields(self):
        answer = Answer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id']:
            self.assertIn(field, fields)


class NumericalAnswerTest(TestCase):

    def test_numerical_answer_fields(self):
        answer = NumericalAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response']:
            self.assertIn(field, fields)

    def test_numerical_answer_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Number')
        country = Country.objects.create(name="Peru")
        answer = NumericalAnswer.objects.create(question=question, country=country, response=11.2)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(11.2, answer.response)

    def test_numerical_answer_cannot_be_text(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Number')
        country = Country.objects.create(name="Peru")
        answer = NumericalAnswer(question=question, country=country, response='not a decimal number')
        self.assertRaises(ValidationError, answer.save)


class TextAnswerTest(TestCase):

    def test_text_answer_fields(self):
        answer = TextAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response']:
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

    def test_date_answer_fields(self):
        answer = DateAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'question_id','country_id', 'response']:
            self.assertIn(field, fields)

    def test_date_answer_store(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Date')
        country = Country.objects.create(name="Peru")
        some_date = date.today()
        answer = DateAnswer.objects.create(question=question, country=country, response=some_date)
        self.failUnless(answer.id)
        self.assertEqual(question, answer.question)
        self.assertEqual(country, answer.country)
        self.assertEqual(some_date, answer.response)

    def test_date_answer_can_only_be_date(self):
        question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Date')
        country = Country.objects.create(name="Peru")
        not_date = 'hahaha'
        answer = DateAnswer(question=question, country=country, response=not_date)
        self.assertRaises(ValidationError, answer.save)


class MultiChoiceAnswerTest(TestCase):

    def test_mulitchoice_answer_fields(self):
        answer = MultiChoiceAnswer()
        fields = [str(item.attname) for item in answer._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'question_id', 'country_id', 'response_id']:
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
