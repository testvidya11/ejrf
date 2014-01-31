from questionnaire.features.pages.base import PageObject


class LoginPage(PageObject):
    url = "/accounts/login/"

    def login(self, user, password):
        details = {'username': user.username,
                   'password': password,}

        self.browser.fill_form(details)
        self.submit()


class UserListingPage(PageObject):
    url = "/users/"


class CreateUserPage(PageObject):
    url = "/users/new/"

    def select(self, value):
        self.browser.find_by_value(value).first.check()