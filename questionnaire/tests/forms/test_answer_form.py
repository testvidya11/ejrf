from questionnaire.forms.answers import NumericalAnswerForm, TextAnswerForm, DateAnswerForm
from questionnaire.models import Question, Country
from questionnaire.tests.base_test import BaseTest


class NumericalAnswerFormTest(BaseTest):
    def setUp(self):
        self.country = Country.objects.create(name="Peru")
        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00004', answer_type='Number')

        self.form_data = {
            'question': self.question3.id,
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
        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00004', answer_type='Number')

        self.form_data = {
            'question': self.question3.id,
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
        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00004', answer_type='Number')

        self.form_data = {
            'question': self.question3.id,
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
