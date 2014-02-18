from questionnaire.features.pages.base import PageObject


class QuestionListingPage(PageObject):
    url = "/questions/"


class CreateQuestionPage(PageObject):
    url = "/questions/new/"

    def remove_option_field(self, selector, number):
        self.browser.find_by_css(selector)[number].click()

    def fill_first_visible_option(self, name, value):
        self.browser.find_by_name(name).last.fill(value)