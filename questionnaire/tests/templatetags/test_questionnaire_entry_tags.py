from django.test import Client
from questionnaire.templatetags.questionnaire_entry_tags import get_form
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryTagTest(BaseTest):

    def test_get_form(self):
        fake_question = 'some question object'
        fake_ordered_forms = {fake_question: 'Fake form'}

        self.assertEqual('Fake form', get_form(fake_question, fake_ordered_forms))
