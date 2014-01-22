from questionnaire.models.locations import Region, Country, Organization
from questionnaire.tests.base_test import BaseTest


class RegionTest(BaseTest):

    def test_region_fields(self):
        region = Region()
        fields = [str(item.attname) for item in region._meta.fields]
        self.assertEqual(6, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description', 'organization_id']:
            self.assertIn(field, fields)

    def test_store(self):
        org = Organization.objects.create(name="WHO")
        region = Region.objects.create(name="Region", organization=org)
        self.failUnless(region.id)
        self.assertEqual(org, region.organization)
        self.assertIsNone(region.description)


class CountryTest(BaseTest):

    def test_country_fields(self):
        country = Country()
        fields = [str(item.attname) for item in country._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'code']:
            self.assertIn(field, fields)

    def test_store(self):
        paho = Region.objects.create(name="PAHO")
        country = Country.objects.create(name="Peru")
        country.regions.add(paho)
        self.failUnless(country.id)
        regions = country.regions.all()
        self.assertEqual(1,regions.count() )
        self.assertIn(paho,regions )


class OrgTest(BaseTest):

    def test_org_fields(self):
        org = Organization()
        fields = [str(item.attname) for item in org._meta.fields]
        self.assertEqual(4, len(fields))
        for field in ['id', 'created', 'modified', 'name']:
            self.assertIn(field, fields)

    def test_store(self):
        org = Organization.objects.create(name="WHO")
        self.failUnless(org.id)
        self.assertEqual("WHO", org.name)
