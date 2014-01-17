from questionnaire.forms.locations import RegionForm
from questionnaire.models import Organization
from questionnaire.tests.base_test import BaseTest


class LocationTypeFormTest(BaseTest):
    def setUp(self):
        org = Organization.objects.create(name="WHO")
        self.form_data = {
            'name': 'AFRO',
            'description': 'All African countries',
            'organization': org.id
        }

    def test_valid(self):
        region_form = RegionForm(self.form_data)
        self.assertTrue(region_form.is_valid())

    def test_invalid(self):
        form_data = self.form_data.copy()
        form_data['name'] = ''
        region_form = RegionForm(form_data)
        self.assertFalse(region_form.is_valid())
        message = 'This field is required.'
        self.assertEqual([message], region_form.errors['name'])
