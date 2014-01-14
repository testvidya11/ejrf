from questionnaire.features.pages.base import PageObject


class ListRegionsPage(PageObject):
    url = '/locations/region/'

    def _assert_table_headers(self):
        pass

    def validate_region_list(self, regions):
        self._assert_table_headers()
        for region in regions:
            for attribute in ['name', 'description']:
                self.is_text_present(str(getattr(region, attribute)))