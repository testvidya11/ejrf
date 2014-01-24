from questionnaire.templatetags.general_template_tags import display_list
from questionnaire.tests.base_test import BaseTest


class GeneralTemplateTagTest(BaseTest):

    def test_display_list_tag(self):
        sample_list = ['Global', 'Regional', 'Epi Manager']
        self.assertEqual(', '.join(sample_list), display_list(sample_list))