from questionnaire.features.pages.base import PageObject


class ListRegionsPage(PageObject):
    url = '/locations/region/'

    def validate_region_list(self, regions):
        self.is_text_present("Name", "Organization", "Description")
        for region in regions:
            for attribute in ['name', 'organization', 'description']:
                self.is_text_present(str(getattr(region, attribute)))

class ListCountriesPage(PageObject):

    def __init__(self, browser, region):
        self.browser = browser
        self.region = region
        self.url = '/locations/region/%d/country/' % region.id

    def validate_country_list(self, countries):
        self.is_text_present("Name", "Region")
        for country in countries:
            self.is_text_present(country.name)