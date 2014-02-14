from django.test import Client
from questionnaire.models import Region, Country, Questionnaire, Section
from questionnaire.tests.base_test import BaseTest


class SectionsViewTest(BaseTest):

    def setUp(self):
        self.client = Client()
        self.user, self.country = self.create_user_with_no_permissions()

        self.assign('can_submit_responses', self.user)
        self.client.login(username=self.user.username, password='pass')

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", year=2013)
        self.url = '/questionnaire/entry/%s/section/new/' % self.questionnaire.id
        self.form_data = {'name': 'New section',
                          'description': 'funny section',
                          'title': 'some title',
                          'questionnaire': self.questionnaire.id
                        }


    def test_get_create_section(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/sections/new.html', templates)

    def test_post_create_section(self):
        self.failIf(Section.objects.filter(**self.form_data))
        response = self.client.post(self.url, data=self.form_data)
        section = Section.objects.get(**self.form_data)
        self.failUnless(section)
        self.assertRedirects(response,expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id ,section.id))

    def test_post_with_form_increments_order_before_saving(self):
        Section.objects.create(name="Some", order=1, questionnaire=self.questionnaire)
        form_data = self.form_data.copy()
        form_data['name'] = 'Another section'
        self.failIf(Section.objects.filter(**form_data))
        response = self.client.post(self.url, data=form_data)
        section = Section.objects.get(order=2, name=form_data['name'])
        self.failUnless(section)
        self.assertRedirects(response,expected_url='/questionnaire/entry/%s/section/%s/' % (self.questionnaire.id ,section.id))