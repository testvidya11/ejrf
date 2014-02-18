from questionnaire.forms.questions import QuestionForm
from questionnaire.models import Question, QuestionOption
from questionnaire.tests.base_test import BaseTest


class QuestionsFormTest(BaseTest):

    def setUp(self):
        self.form_data = {'text': 'How many kids were immunised this year?',
                          'instructions': 'Some instructions',
                          'short_instruction': 'short version',
                          'answer_type': 'Number',
                          'options': ['', ]}

    def test_valid(self):
        section_form = QuestionForm(data=self.form_data)
        self.assertTrue(section_form.is_valid())

    def test_increments_uid_of_existing_question_by_one_upon_save_given_instance(self):
        Question.objects.create(text='B. Number of cases tested',
                                instructions="Enter the total number of cases", UID='00001', answer_type='Number')
        section_form = QuestionForm(data=self.form_data)
        question = section_form.save(commit=True)
        self.assertEqual('00002', question.UID)

    def test_invalid_if_question_text_is_blank(self):
        data = self.form_data.copy()
        data['text'] = ''
        section_form = QuestionForm(data=data)
        self.assertFalse(section_form.is_valid())
        self.assertIn("This field is required.", section_form.errors['text'])

    def test_answer_type_choices_has_empty_label(self):
        section_form = QuestionForm()
        self.assertIn(('', 'Answer type'), section_form.fields['answer_type'].choices)

    def test_save_multichoice_question_saves_options(self):
        options = ['Yes', 'No', 'Maybe']
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'answer_type': 'MultiChoice',
                'options': options}

        section_form = QuestionForm(data=form)
        question = section_form.save(commit=True)
        question_options = QuestionOption.objects.filter(question=question)

        self.assertEqual(3, question_options.count())
        [self.assertIn(question_option.text, options) for question_option in question_options]

    def test_form_invalid_if_multichoice_question_and_no_options_in_data_options(self):
        form = {'text': 'How many kids were immunised this year?',
                'instructions': 'Some instructions',
                'short_instruction': 'short version',
                'answer_type': 'MultiChoice',
                'options': ['', ]}

        section_form = QuestionForm(data=form)

        self.assertFalse(section_form.is_valid())
        message = "MultiChoice questions must have at least one option"
        self.assertIn(message, section_form.errors['__all__'][0])