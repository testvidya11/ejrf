from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from lettuce import step, world
from questionnaire.features.pages.extract import ExtractPage
from questionnaire.features.pages.home import HomePage
from questionnaire.features.pages.users import LoginPage, UserListingPage, CreateUserPage
from questionnaire.models import Region, Country, UserProfile


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
    world.page.is_text_present("Electronic Joint Reporting Form")

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
    world.page.is_text_present("Username, password mismatch. Please try again.")

@step(u'When I click the logout link')
def when_i_click_the_logout_link(step):
    world.page.click_link_by_partial_href("/accounts/logout/")


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
    world.global_admin = Group.objects.create(name='Global Admin')
    auth_content = ContentType.objects.get_for_model(Permission)
    permission, out = Permission.objects.get_or_create(codename='is_global_admin', content_type=auth_content)
    world.global_admin.permissions.add(permission)
    world.global_admin.user_set.add(world.user)

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
    world.page.validate_user_list_headers()
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
    world.page.select(world.global_admin.id)

@step(u'Then I should see that the user was successfully created')
def then_i_should_see_that_the_user_was_successfully_created(step):
    world.page.is_text_present("User created successfully.")

@step(u'And I should see the user listed on the listing page')
def and_i_should_see_the_user_listed_on_the_listing_page(step):
    world.page.is_text_present(world.form_data['username'], world.form_data['email'], world.global_admin.name)

@step(u'And I have a region')
def and_i_have_a_region(step):
    world.afro_region = Region.objects.create(name="Afro")

@step(u'And I have 10 users in one of the regions')
def and_i_have_10_users_in_one_region(step):
    for i in range(0, 10):
        world.user = User.objects.create(username='Rajni%s' % str(i), email='rajni@kant%s.com' % str(i), password='I_Rock')
        world.country = Country.objects.create(name="Country%s" % str(i), code="UGX")
        world.afro_region.countries.add(world.country)
        UserProfile.objects.create(user=world.user, country=world.country, region=world.afro_region)

@step(u'And I have five others not in that region')
def and_i_have_five_others_not_in_that_region(step):
    region = Region.objects.create(name="Afro")
    for i in range(11, 16):
        world.user = User.objects.create(username='Jacinta%s' % str(i), email='jacinta%s@gmail.com' % str(i), password='I_Rock')
        UserProfile.objects.create(user=world.user, region=region)


@step(u'And I select a region')
def and_i_select_a_region(step):
    world.page.select(world.afro_region.id)

@step(u'And I click get list')
def and_i_click_get_list(step):
    world.page.click_by_css("#get-list-btn")

@step(u'Then I should see only the users in that region')
def then_i_should_see_only_the_users_in_that_region(step):
    for i in range(0, 10):
        world.page.is_text_present('Rajni%s' % str(i), 'rajni@kant%s.com' % str(i))

    for i in range(11, 16):
        world.page.is_text_present('Jacinta%s' % str(i), 'jacinta%s@gmail.com' % str(i), status=False)