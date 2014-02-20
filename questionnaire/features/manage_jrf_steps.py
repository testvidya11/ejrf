from lettuce import world, step
from questionnaire.features.pages.home import HomePage
from questionnaire.models import Questionnaire, Section


@step(u'Given I have four finalised questionnaires')
def given_i_have_four_finalised_questionnaires(step):
    world.questionnaire1 = Questionnaire.objects.create(name="JRF Jamaica version", description="description",
                                                        year=2012, finalized=True)

    Section.objects.create(title="School Based Section1", order=0, questionnaire=world.questionnaire1, name="Name")

    world.questionnaire2 = Questionnaire.objects.create(name="JRF Brazil version", description="description",
                                                        year=2013, finalized=True)
    Section.objects.create(title="School Section1", order=0, questionnaire=world.questionnaire2, name="Section1 name")
    world.questionnaire3 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2013, finalized=True)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire3, name="School Imm. Delivery")
    world.questionnaire4 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=2013, finalized=True)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire4, name="School Imm. Delivery")


@step(u'And I have two draft questionnaires for two years')
def and_i_have_two_draft_questionnaires_for_two_years(step):
    world.questionnaire5 = Questionnaire.objects.create(name="JRF Bolivia version", description="some more description",
                                                        year=2013, finalized=False)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire5, name="School Imm. Delivery")
    world.questionnaire6 = Questionnaire.objects.create(name="JRF kampala version", description="description",
                                                        year=2013, finalized=False)
    Section.objects.create(title="Section1", order=0, questionnaire=world.questionnaire6, name="School Imm. Delivery")


@step(u'Then I should see manage JRF, users, question bank, extract and attachments links')
def then_i_should_see_manage_jrf_users_question_bank_extract_and_attachments_links(step):
    world.page.is_text_present("HOME", "EXTRACT", "ATTACHMENTS", "MANAGE JRF", "USERS", "QUESTION BANK")

@step(u'And I should see a list of finalised questionnaires')
def and_i_should_see_a_list_of_finalised_questionnaires(step):
    world.page = HomePage(world.browser)
    world.page.links_present_by_text(["%s %s" % (world.questionnaire1.name, world.questionnaire1.year),
                                     "%s %s" % (world.questionnaire2.name, world.questionnaire2.year),
                                     "%s %s" % (world.questionnaire3.name, world.questionnaire3.year),
                                     "%s %s" % (world.questionnaire4.name, world.questionnaire4.year)])

@step(u'And I should see a list of draft questionnaires')
def and_i_should_see_a_list_of_draft_questionnaires(step):
    world.page.links_present_by_text(["%s %s" % (world.questionnaire6.name, world.questionnaire6.year),
                                     "%s %s" % (world.questionnaire5.name, world.questionnaire5.year)])
    world.page.links_present_by_text([" Edit", " Finalize"])

@step(u'And I visit manage JRF page')
def and_i_visit_manage_jrf_page(step):
    world.page.click_by_id('id-manage-jrf')