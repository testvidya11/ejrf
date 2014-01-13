from django.test import TestCase
from questionnaire.forms.locations import LocationTypeForm
from questionnaire.models import LocationType


class LocationTypeFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            'name': 'REGION',
            'order': 1,
            'description': 'description goes here',
        }

    def test_valid(self):
        location_type = LocationTypeForm(self.form_data)
        self.assertTrue(location_type.is_valid())

    def test_invalid(self):
        form_data = self.form_data.copy()
        form_data['order'] = ''
        location_type = LocationTypeForm(form_data)
        self.assertFalse(location_type.is_valid())
        message = 'This field is required.'
        self.assertEqual([message], location_type.errors['order'])

    def test_duplicate_order_is_invalid(self):
        LocationType.objects.create(name="Region", order=1)
        form_data = self.form_data.copy()
        form_data['order'] = 1
        location_type = LocationTypeForm(form_data)
        self.assertFalse(location_type.is_valid())
        message = 'Location type with this Order already exists.'
        self.assertEqual([message], location_type.errors['order'])