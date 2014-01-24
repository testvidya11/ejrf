from questionnaire.features.pages.base import PageObject


class LoginPage(PageObject):
    url = "/accounts/login/"


class UserListingPage(PageObject):
    url = "/users/"


class CreateUserPage(PageObject):
    url = "/users/new/"