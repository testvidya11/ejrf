from lettuce import step, world
from questionnaire.features.pages.locations import ListRegionsPage, ListCountriesPage
from questionnaire.models.locations import Region, Country, Organization


@step(u'Given I have two regions')
def given_i_have_two_regions(step):
    world.org = Organization.objects.create(name="WHO")
    world.afro = Region.objects.create(name="AFRO", organization=world.org)
    world.paho = Region.objects.create(name="PAHO", organization=world.org)

@step(u'And I visit the list regions page')
def and_i_visit_the_list_regions_page(step):
    world.page = ListRegionsPage(world.browser)
    world.page.visit()

@step(u'Then I should see the list of regions')
def then_i_should_see_the_list_of_regions(step):
    world.page.validate_region_list([world.afro, world.paho])

@step(u'Given I have two countries in a region')
def given_i_have_two_countries_in_a_region(step):
    world.afro = Region.objects.create(name="AFRO")
    world.uganda = Country.objects.create(name="Uganda", region=world.afro)
    world.kenya = Country.objects.create(name="Kenya", region=world.afro)

@step(u'And I visit the list countries page in that region')
def and_i_visit_the_list_countries_page_in_that_region(step):
    world.page = ListCountriesPage(world.browser, world.afro)
    world.page.visit()

@step(u'Then I should see the list of countries in that region')
def then_i_should_see_the_list_of_countries_in_that_region(step):
    world.page.validate_country_list([world.uganda, world.kenya])
