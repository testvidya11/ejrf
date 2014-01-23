from django.test import Client
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup
from questionnaire.services.questionnaire_entry_form_service import QuestionnaireEntryFormService
from questionnaire.tests.base_test import BaseTest


class QuestionnaireEntryViewTest(BaseTest):

    def setUp(self):
        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                      questionnaire=self.questionnaire, name="Reported Cases")

        self.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=self.section_1)

        self.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
        self.question2 = Question.objects.create(text='B. Number of cases tested',
                                    instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                    UID='C00003', answer_type='Number')

        self.question3 = Question.objects.create(text='C. Number of cases positive',
                                            instructions="Include only those cases found positive for the infectious agent.",
                                            UID='C00004', answer_type='Number')

        self.question_group = QuestionGroup.objects.create(subsection=self.sub_section, order=1)
        self.question_group.question.add(self.question1, self.question3, self.question2)


        self.client = Client()

    def test_get_questionnaire_entry_view(self):
        response = self.client.get('/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id))
        self.assertEqual(200, response.status_code)
        templates = [template.name for template in response.templates]
        self.assertIn('questionnaires/entry/index.html', templates)
        self.assertEqual(self.questionnaire, response.context['questionnaire'])
        self.assertEqual(self.section_1, response.context['section'])
        self.assertIsInstance(response.context['formsets'], QuestionnaireEntryFormService)

    def test_gets_ordered_sections_for_menu_breadcrumps_wizzard(self):
        section2 = Section.objects.create(title="section 2", order=2, questionnaire=self.questionnaire)
        section3 = Section.objects.create(title="section 3", order=3, questionnaire=self.questionnaire)
        response = self.client.get('/questionnaire/entry/%d/section/%d/' % (self.questionnaire.id, self.section_1.id))
        self.assertEqual(200, response.status_code)
        self.assertEqual(3, response.context['ordered_sections'].count())
        self.assertEqual(self.section_1, response.context['ordered_sections'][0])
        self.assertEqual(section2, response.context['ordered_sections'][1])
        self.assertEqual(section3, response.context['ordered_sections'][2])
