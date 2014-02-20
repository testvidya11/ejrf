from questionnaire.features.pages.base import PageObject


class HomePage(PageObject):
    url = "/"

    def links_present_by_text(self, links_text):
        for text in links_text:
            assert self.browser.find_link_by_text(text)