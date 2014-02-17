from questionnaire.features.pages.base import PageObject


class CreateSectionPage(PageObject):
    def __init__(self, browser, questionnaire):
        super(CreateSectionPage, self).__init__(browser)
        self.url = '/questionnaire/entry/%s/section/new/' % questionnaire.id

class CreateSubSectionPage(PageObject):
    def __init__(self, browser, questionnaire, section):
        super(CreateSubSectionPage, self).__init__(browser)
        self.url = '/questionnaire/entry/%s/section/%s/subsection/new/' % (questionnaire.id, section.id)

