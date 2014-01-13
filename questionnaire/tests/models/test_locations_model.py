from django.test import TestCase
from questionnaire.models.locations import LocationType


class LocationTypeTest(TestCase):

    def test_location_type_fields(self):
        region = LocationType()
        fields = [str(item.attname) for item in region._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description', 'order']:
            self.assertIn(field, fields)
