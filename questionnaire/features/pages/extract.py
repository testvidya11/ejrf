from questionnaire.features.pages.base import PageObject


class ExtractPage(PageObject):
    url = '/extract/'

    def extract_button_present(self):
        assert self.browser.find_by_id('export-data')