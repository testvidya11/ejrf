from django.test import TestCase
from questionnaire.forms.locations import RegionForm


class LocationTypeFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            'name': 'AFRO',
            'description': 'All African countries',
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
