from lettuce import step, world
from questionnaire.features.pages.locations import ListRegionsPage
from questionnaire.models.locations import Region


@step(u'Given I have three location types')
def given_i_have_three_location_types(step):
    world.afro = Region.objects.create(name="AFRO")
    world.paho = Region.objects.create(name="PAHO")


@step(u'And I visit the list location types page')
def and_i_visit_the_list_location_types_page(step):
    world.page = ListRegionsPage(world.browser)
    world.page.visit()

@step(u'Then I should see the list of location types')
def then_i_should_see_the_list_of_location_types(step):
    world.page.validate_region_list([world.afro, world.paho])