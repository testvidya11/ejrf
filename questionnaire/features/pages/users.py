from questionnaire.features.pages.base import PageObject


class LoginPage(PageObject):
    url = "/accounts/login/"

    def fill_form(self, data):
        self.browser.fill_form(data)