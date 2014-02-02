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

    def validate_user_list_headers(self):
        self.is_text_present("Username", "Email", "Roles", "Organization / Region / Country", "Status", "Actions")


class CreateUserPage(PageObject):
    url = "/users/new/"
