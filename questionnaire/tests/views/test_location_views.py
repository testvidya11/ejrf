from django.test import Client
from questionnaire.models import LocationType
from questionnaire.tests.base_test import BaseTest


class LocationTypeViewTest(BaseTest):

    def setUp(self):
        self.client = Client()

    def test_get_location_type_list(self):
        region = LocationType.objects.create(name="Region", order=1)
        response = self.client.get('/locations/type/')
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('locations/type/index.html', templates)
        self.assertEqual(1, len(response.context['locationtype_list']))
        self.assertIn(region, response.context['locationtype_list'])
