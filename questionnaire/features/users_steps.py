from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from lettuce import step, world
from questionnaire.features.pages.extract import ExtractPage
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.users import LoginPage, UserListingPage, CreateUserPage
from questionnaire.models import UserProfile


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
    world.page.is_text_present("Ooops! Your username or password is incorrect. Please try again.")

@step(u'When I click the logout link')
def when_i_click_the_logout_link(step):
    world.page.click_link_by_partial_href("/logout/")


@step(u'Then I should see the login page again')
def then_i_should_see_the_login_page_again(step):
    world.page = LoginPage(world.browser)
    world.page.validate_url()

@step(u'Given I visit the extract page')
def given_i_visit_the_extract_page(step):
    world.page = ExtractPage(world.browser)
    world.page.visit()

@step(u'When I fill in the login credentials')
def when_i_fill_in_the_login_credentials(step):
    world.page = LoginPage(world.browser)
    data = {'username': world.user.username,
            'password': "pass"}
    world.page.fill_form(data)

@step(u'Then I should see the extract page')
def then_i_should_see_the_extract_page(step):
    world.page = ExtractPage(world.browser)

@step(u'Given I have a global admin user')
def given_i_have_a_global_admin_user(step):
    world.user = User.objects.create(username='user1', email='rajni@kant.com')
    world.user.set_password('pass')
    world.user.save()
    global_admin = Group.objects.create(name='Global Admin')
    auth_content = ContentType.objects.get_for_model(Permission)
    permission, out = Permission.objects.get_or_create(codename='is_global_admin', content_type=auth_content)
    global_admin.permissions.add(permission)
    global_admin.user_set.add(world.user)

@step(u'And I have 100 other users')
def and_i_have_100_other_users(step):
    for i in range(0, 100):
        User.objects.create(username='Rajni%s' % str(i), email='rajni@kant%s.com' % str(i), password='I_Rock')

@step(u'And I visit the user listing page')
def and_i_visit_the_user_listing_page(step):
    world.page = UserListingPage(world.browser)
    world.page.visit()

@step(u'Then I should see the list of users paginated')
def then_i_should_see_the_list_of_users_paginated(step):
    world.page.validate_pagination()

@step(u'And I click an new user button')
def and_i_click_an_new_user_button(step):
    world.page.click_by_css("#add-new-user")
    world.page = CreateUserPage(world.browser)

@step(u'And I fill in the user information')
def and_i_fill_in_the_user_information(step):
    world.form_data = {
        'username': 'rajni',
        'password1': 'kant',
        'password2': 'kant',
        'email': 'raj@ni.kant'}
    world.page.fill_form(world.form_data)

@step(u'Then I should see that the user was successfully created')
def then_i_should_see_that_the_user_was_successfully_created(step):
    world.page.is_text_present("User created successfully.")

@step(u'And I should see the user listed on the listing page')
def and_i_should_see_the_user_listed_on_the_listing_page(step):
    world.page.is_text_present(world.form_data['username'], world.form_data['email'])

@step(u'And I have 10 other users')
def and_i_have_10_other_users(step):
    for i in range(0, 10):
        User.objects.create(username='Rajni%s' % str(i), email='rajni@kant%s.com' % str(i), password='I_Rock')