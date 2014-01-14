from django.test import TestCase
from questionnaire.models.locations import Region


class RegionTest(TestCase):

    def test_region_fields(self):
        region = Region()
        fields = [str(item.attname) for item in region._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description']:
            self.assertIn(field, fields)

    def test_store(self):
        region = Region.objects.create(name="Region")
        self.failUnless(region.id)
        self.assertIsNone(region.description)