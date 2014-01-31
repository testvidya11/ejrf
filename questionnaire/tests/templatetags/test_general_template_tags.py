from questionnaire.templatetags.general_template_tags import display_list, bootstrap_message
from questionnaire.tests.base_test import BaseTest


class GeneralTemplateTagTest(BaseTest):

    def test_display_list_tag(self):
        sample_list = ['Global', 'Regional', 'Epi Manager']
        self.assertEqual(', '.join(sample_list), display_list(sample_list))

    def test_message(self):
        self.assertEqual('success', bootstrap_message('success'))
        self.assertEqual('danger', bootstrap_message('error'))
        self.assertEqual('warning', bootstrap_message('warning'))