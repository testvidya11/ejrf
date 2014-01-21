from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm, MultiChoiceAnswerForm
from questionnaire.models import Question, Country, QuestionOption
from questionnaire.tests.base_test import BaseTest


class NumericalAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='Number')

        self.form_data = {
            'question': self.question.id,
            'country': self.country.id,
            'status': 'DRAFT',
            'version':1,
            'response':100
            
        }

    def test_valid(self):
        answer_form = NumericalAnswerForm(self.form_data)
        self.assertTrue(answer_form.is_valid())

    def test_text_response_is_invalid(self):
        form_data = self.form_data.copy()
        form_data['response'] = 'some text which is not number'
        answer_form = NumericalAnswerForm(form_data)
        self.assertFalse(answer_form.is_valid())
        message = 'Enter a number.'
        self.assertEqual([message], answer_form.errors['response'])


class TextAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='Text')

        self.form_data = {
            'question': self.question.id,
            'country': self.country.id,
            'status': 'DRAFT',
            'version':1,
            'response':'some answer'
        }

    def test_valid(self):
        answer_form = TextAnswerForm(self.form_data)
        self.assertTrue(answer_form.is_valid())

    def test_version_should_be_integer(self):
        form_data = self.form_data.copy()
        form_data['version'] = 'some text which is not number'
        answer_form = TextAnswerForm(form_data)
        self.assertFalse(answer_form.is_valid())
        message = 'Enter a whole number.'
        self.assertEqual([message], answer_form.errors['version'])

class DateAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='Date')

        self.form_data = {
            'question': self.question.id,
            'country': self.country.id,
            'status': 'DRAFT',
            'version':1,
            'response':'2014-01-01'
        }

    def test_valid(self):
        answer_form = DateAnswerForm(self.form_data)
        self.assertTrue(answer_form.is_valid())

    def test_response_cannot_be_text(self):
        form_data = self.form_data.copy()
        form_data['response'] = 'some text which is not a date'
        answer_form = DateAnswerForm(form_data)
        self.assertFalse(answer_form.is_valid())
        message = 'Enter a valid date.'
        self.assertEqual([message], answer_form.errors['response'])

class MultiChoiceAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00001', answer_type='MultiChoice')
        question_option_one = QuestionOption.objects.create(text='Option One', question=self.question)

        self.form_data = {
            'question': self.question.id,
            'country': self.country.id,
            'status': 'DRAFT',
            'version':1,
            'response': question_option_one.id
        }

    def test_valid(self):
        answer_form = MultiChoiceAnswerForm(self.form_data)
        self.assertTrue(answer_form.is_valid())

    def test_id_of_a_non_option(self):
        form_data = self.form_data.copy()
        form_data['response'] = -1
        answer_form = MultiChoiceAnswerForm(form_data)
        self.assertFalse(answer_form.is_valid())
        message = 'Select a valid choice. That choice is not one of the available choices.'
        self.assertEqual([message], answer_form.errors['response'])
