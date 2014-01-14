from django.test import Client
from questionnaire.models import Region
from questionnaire.tests.base_test import BaseTest


class LocationTypeViewTest(BaseTest):

    def setUp(self):
        self.client = Client()

    def test_get_region_list(self):
        region = Region.objects.create(name="AFRO")
        response = self.client.get('/locations/region/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('locations/region/index.html', templates)
        self.assertEqual(1, len(response.context['region_list']))
        self.assertIn(region, response.context['region_list'])
