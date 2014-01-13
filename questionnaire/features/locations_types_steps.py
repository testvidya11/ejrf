from lettuce import step, world
from questionnaire.features.pages.locations import ListLocationTypesPage
from questionnaire.models.locations import LocationType


@step(u'Given I have three location types')
def given_i_have_three_location_types(step):
    world.world_ = LocationType.objects.create(name="World", order=0)
    world.region = LocationType.objects.create(name="Region", order=1)
    world.country = LocationType.objects.create(name="Country", order=2)


@step(u'And I visit the list location types page')
def and_i_visit_the_list_location_types_page(step):
    world.page = ListLocationTypesPage(world.browser)
    world.page.visit()

@step(u'Then I should see the list of location types')
def then_i_should_see_the_list_of_location_types(step):
    world.page.validate_list_location_types([world.world_, world.region, world.country])