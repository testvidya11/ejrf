from questionnaire.forms.filter import UserFilterForm
from questionnaire.models import Region, Organization
from questionnaire.tests.base_test import BaseTest


class UserProfileFormTest(BaseTest):

    def setUp(self):
        self.region = Region.objects.create(name="Afro")
        self.organization = Organization.objects.create(name="UNICEF")
        self.form_data = {
            'region': self.region.id,
            'organization': self.organization.id,
        }

    def test_valid(self):
        user_filter = UserFilterForm(self.form_data)
        self.assertTrue(user_filter.is_valid())