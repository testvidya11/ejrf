from django.contrib.auth.models import User
from lettuce import step, world
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.users import LoginPage

@step(u'Given I am registered user')
def given_i_am_registered_user(step):
    world.user = User.objects.create(username="user", email="user@mail.com")
    world.user.set_password("pass")
    world.user.save()

@step(u'And I visit the login page')
def and_i_visit_the_login_page(step):
    world.page = LoginPage(world.browser)
    world.page.visit()

@step(u'And I fill in the login credentials')
def and_i_fill_in_the_login_credentials(step):
    data = {'username': world.user.username,
            'password': "pass"}
    world.page.fill_form(data)

@step(u'And I submit the form')
def and_i_submit_the_form(step):
    world.page.submit()

@step(u'Then I should be redirected home page')
def then_i_should_be_redirected_dashboard(step):
    world.page = HomePage(world.browser)
    world.page.validate_url()

@step(u'And I should see my username and the logout link')
def and_i_should_see_my_username_and_the_logout_link(step):
    world.page.is_text_present(world.user.get_username(), "Logout")

@step(u'Given I visit the login page')
def given_i_visit_the_login_page(step):
    world.page = LoginPage(world.browser)
    world.page.visit()

@step(u'And I fill in invalid user credentials')
def and_i_fill_in_invalid_user_credentials(step):
    data = {'username': "invalid username",
            'password': "pass"}
    world.page.fill_form(data)

@step(u'Then I should see an error message')
def then_i_should_see_an_error_message(step):
    world.page.is_text_present("Your username or password is incorrect. Please try again")

@step(u'When I click the logout link')
def when_i_click_the_logout_link(step):
    world.page.click_link_by_partial_href("/logout/")


@step(u'Then I should see the login page again')
def then_i_should_see_the_login_page_again(step):
    world.page = LoginPage(world.browser)
    world.page.validate_url()