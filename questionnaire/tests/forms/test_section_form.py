from questionnaire.forms.sections import SectionForm
from questionnaire.models import Questionnaire, Section
from questionnaire.tests.base_test import BaseTest


class CoreSectionFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.form_data = {'name': 'New section',
                          'order': 1,
                          'description': 'funny section',
                          'title': 'some title',
                          'questionnaire': self.questionnaire.id}

    def test_valid(self):
        section_form = SectionForm(initial={'questionnaire': self.questionnaire.id}, data=self.form_data)
        self.assertTrue(section_form.is_valid())

    def test_valid_with_initial(self):
        section_form = SectionForm(data=self.form_data, initial={'questionnaire': self.questionnaire.id})
        self.assertTrue(section_form.is_valid())

    def test_invalid_if_order_is_taken(self):
        Section.objects.create(name="Some section", order=1, questionnaire=self.questionnaire)
        data = self.form_data.copy()
        data['order'] = 1
        section_form = SectionForm(data=data, initial={'questionnaire': self.questionnaire.id})
        self.assertFalse(section_form.is_valid())
        message = "Orders should be unique"
        self.assertIn(message, section_form.errors['order'])