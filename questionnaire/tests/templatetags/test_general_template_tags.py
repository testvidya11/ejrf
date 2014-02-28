from questionnaire.templatetags.generic_tags import display_list, bootstrap_message, get_url_with_ids, divide_to_paginate, ASSIGN_QUESTION_PAGINATION_SIZE
from questionnaire.tests.base_test import BaseTest


class GeneralTemplateTagTest(BaseTest):

    def test_display_list_tag(self):
        sample_list = ['Global', 'Regional', 'Epi Manager']
        self.assertEqual(', '.join(sample_list), display_list(sample_list))

    def test_message(self):
        self.assertEqual('success', bootstrap_message('success'))
        self.assertEqual('danger', bootstrap_message('error'))
        self.assertEqual('warning', bootstrap_message('warning'))

    def test_should_return_url_given_url_name_and_ids(self):
        self.assertEqual('/questionnaire/document/1/delete/', get_url_with_ids(1, 'delete_document'))
        self.assertEqual('/questionnaire/entry/1/section/2/', get_url_with_ids("1, 2", 'questionnaire_entry_page'))

    def test_should_divide_questions_per_30(self):
        arbitrary_number = 220
        original_list = range(arbitrary_number)
        for i in range(1 + arbitrary_number / ASSIGN_QUESTION_PAGINATION_SIZE):
            paginated_list = range(i* ASSIGN_QUESTION_PAGINATION_SIZE, min((i+1)* ASSIGN_QUESTION_PAGINATION_SIZE, len(original_list)))
            self.assertEqual(paginated_list, divide_to_paginate(original_list)[i])