from questionnaire.features.pages.base import PageObject


class CreateSectionPage(PageObject):
    def __init__(self, browser, questionnaire):
        super(CreateSectionPage, self).__init__(browser)
        self.url = '/questionnaire/entry/%s/section/new/' % questionnaire.id