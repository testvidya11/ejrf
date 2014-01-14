from django.test import TestCase
from questionnaire.models.locations import LocationType, Location
from django.db import IntegrityError


class LocationTypeTest(TestCase):

    def test_location_type_fields(self):
        region = LocationType()
        fields = [str(item.attname) for item in region._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description', 'order']:
            self.assertIn(field, fields)

    def test_store(self):
        region = LocationType.objects.create(name="Region", order=1)
        self.failUnless(region.id)
        self.assertEqual(1, region.order)
        self.assertIsNone(region.description)

    def test_unique_order(self):
        region = LocationType.objects.create(name="Region", order=1)
        another_region = LocationType(name="haha", order=1)
        self.assertRaises(IntegrityError, another_region.save)


class LocationTest(TestCase):

    def test_location_type_fields(self):
        location = Location()
        fields = [str(item.attname) for item in location._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description', 'type_id']:
            self.assertIn(field, fields)

    def test_store(self):
        region = LocationType.objects.create(name="Region", order=1)
        afro = Location.objects.create(name="AFRO", type=region)
        self.failUnless(afro.id)
        self.assertIsNone(afro.description)