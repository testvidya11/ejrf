from datetime import date
from django.contrib.auth.models import Group
from questionnaire.forms.filter import UserFilterForm, QuestionnaireFilterForm
from questionnaire.models import Region, Organization, Questionnaire
from questionnaire.tests.base_test import BaseTest


class UserProfileFormTest(BaseTest):

    def setUp(self):
        self.region = Region.objects.create(name="Afro")
        self.organization = Organization.objects.create(name="UNICEF")
        self.global_admin = Group.objects.create(name="UNICEF")
        self.form_data = {
            'organization': self.organization.id,
            'region': self.region.id,
            'role': self.global_admin.id,
        }

    def test_valid(self):
        user_filter = UserFilterForm(self.form_data)
        self.assertTrue(user_filter.is_valid())

    def test_valid_when_organization_is_blank(self):
        form_data = self.form_data.copy()
        form_data['organization'] = ''
        user_filter = UserFilterForm(form_data)
        self.assertTrue(user_filter.is_valid())

    def test_valid_when_region_is_blank(self):
        form_data = self.form_data.copy()
        form_data['region'] = ''
        user_filter = UserFilterForm(form_data)
        self.assertTrue(user_filter.is_valid())

    def test_valid_when_role_is_blank(self):
        form_data = self.form_data.copy()
        form_data['role'] = ''
        user_filter = UserFilterForm(form_data)
        self.assertTrue(user_filter.is_valid())


class QuestionnaireFilterFormTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=2013)

        self.form_data = {
            'questionnaire': self.questionnaire.id,
            'year': date.today().year + 1,
            'name': 'New JRF'
        }

    def test_valid(self):
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertTrue(questionnaire_filter.is_valid())

    def test_has_years_of_existing_questionnaires(self):
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertIn(('', 'Choose a year'), questionnaire_filter.fields['year'].choices)
        for count in range(0, 10):
            year_option = date.today().year + count
            self.assertIn((year_option, year_option), questionnaire_filter.fields['year'].choices)

    def test_invalid_when_questionniare_is_blank(self):
        form_data = self.form_data.copy()
        form_data['questionnaire'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['questionnaire'])

    def test_invalid_when_year_is_blank(self):
        form_data = self.form_data.copy()
        form_data['year'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['year'])

    def test_valid_when_name_is_blank(self):
        form_data = self.form_data.copy()
        form_data['name'] = ''
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        self.assertIn("This field is required.", questionnaire_filter.errors['name'])

    def test_clean_year(self):
        questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=date.today().year + 1)
        form_data = self.form_data.copy()
        form_data['year'] = questionnaire.year
        questionnaire_filter = QuestionnaireFilterForm(form_data)
        self.assertFalse(questionnaire_filter.is_valid())
        message = "Select a valid choice. %d is not one of the available choices." % questionnaire.year
        self.assertIn(message, questionnaire_filter.errors['year'])

    def test_has_years_choices_exclude_existing_questionnaires_years(self):
        Questionnaire.objects.create(name="JRF 2013 Core English", status=Questionnaire.FINALIZED, year=date.today().year + 1)
        questionnaire_filter = QuestionnaireFilterForm(self.form_data)
        self.assertIn(('', 'Choose a year'), questionnaire_filter.fields['year'].choices)
        for count in range(2, 9):
            year_option = date.today().year + count
            self.assertIn((year_option, year_option), questionnaire_filter.fields['year'].choices)
        self.assertNotIn((date.today().year + 1, date.today().year + 1), questionnaire_filter.fields['year'].choices)