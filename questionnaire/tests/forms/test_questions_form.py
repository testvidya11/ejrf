from questionnaire.forms.questions import QuestionForm
from questionnaire.tests.base_test import BaseTest


class QuestionsFormTest(BaseTest):

    def setUp(self):
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'short_instruction': 'short version',
                          'answer_type': 'Number'}

    def test_valid(self):
        section_form = QuestionForm(data=self.form_data)
        self.assertTrue(section_form.is_valid())