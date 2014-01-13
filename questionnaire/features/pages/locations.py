from questionnaire.features.pages.base import PageObject


class ListLocationTypesPage(PageObject):
    url = '/locations/type/'

    def _assert_table_headers(self):
        pass

    def validate_list_location_types(self, location_types):
        self._assert_table_headers()
        for location_type in location_types:
            for attribute in ['name', 'order']:
                self.is_text_present(str(getattr(location_type, attribute)))