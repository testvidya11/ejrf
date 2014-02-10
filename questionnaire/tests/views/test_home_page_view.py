from urllib import quote
from django.test import Client
from questionnaire.models import Questionnaire, Section
from questionnaire.tests.base_test import BaseTest


class HomePageViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()
        self.login_user()

    def test_get(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('home/index.html', templates)

    def test_homepage_redirects_to_first_section_of_first_questionnaire_if_any(self):
        questionnaire = Questionnaire.objects.create(name="JRF", description="bla")
        section = Section.objects.create(title="section", order=1, questionnaire=questionnaire, name="section")
        section2 = Section.objects.create(title="section", order=2, questionnaire=questionnaire, name="section")

        response = self.client.get("/")
        expected_url = "/questionnaire/entry/%d/section/%d/" % (questionnaire.id, section.id)
        self.assertRedirects(response, expected_url=expected_url)

    def test_login_required_for_home_get(self):
        self.assert_login_required('/')
