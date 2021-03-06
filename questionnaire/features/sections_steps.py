from time import sleep
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.features.pages.sections import CreateSectionPage
from questionnaire.features.pages.users import LoginPage
from questionnaire.models import Country, UserProfile


@step(u'Given I am logged in as a global admin')
def given_i_am_logged_in_as_a_global_admin(step):
    world.uganda = Country.objects.create(name="Uganda")
    user = User.objects.create_user('Rajni', 'rajni@kant.com', 'pass')
    UserProfile.objects.create(user=user, country=world.uganda)
    auth_content = ContentType.objects.get_for_model(Permission)
    group = Group.objects.create(name="Data Submitter")
    permission, out = Permission.objects.get_or_create(codename='can_view_users', content_type=auth_content)
    permission_edit_questionnaire, out = Permission.objects.get_or_create(codename='can_edit_questionnaire',
                                                                          content_type=auth_content)
    group.permissions.add(permission, permission_edit_questionnaire)
    group.user_set.add(user)

    world.page = LoginPage(world.browser)
    world.page.visit()
    world.page.login(user, "pass")

@step(u'And I click add new section link')
def and_i_click_add_new_section_link(step):
    world.page.click_by_id("new-section")

@step(u'Then I should see a new section modal')
def then_i_should_see_a_new_section_modal(step):
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.is_text_present("New Section", "Description", "Name", "Title")

@step(u'When i fill in the section data')
def when_i_fill_in_the_section_data(step):
    data = {'title': 'Some title',
            'description': 'some description'}

    world.page.fill_form(data)
    sleep(3)
    world.page.fill_form({'name': 'Some section'})


@step(u'Then I should see the section I created')
def then_i_should_see_the_section_i_created(step):
    world.page = QuestionnairePage(world.browser, world.section_1)
    world.page.is_text_present('Section created successfully')
    world.page.is_text_present('Some section')

@step(u'And I save the section')
def and_i_save_the_section(step):
    world.page.fill_form({'name': 'Some section'})
    world.page.click_by_id('save-new-section-modal')

@step(u'And I fill in invalid data')
def and_i_fill_in_invalid_data(step):
    data = {'name': '',
            'title': '',
            'description': 'some description'}
    world.page = CreateSectionPage(world.browser, world.questionnaire)
    world.page.fill_form(data)

@step(u'Then I should see error messages against the fields')
def then_i_should_see_error_messages_against_the_fields(step):
    world.page.is_text_present('This field is required')