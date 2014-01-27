from questionnaire.features.pages.base import PageObject


class QuestionnairePage(PageObject):
    def __init__(self, browser, questionnaire):
        super(QuestionnairePage, self).__init__(browser)
        self.questionnaire = questionnaire
        self.section = self.questionnaire.sections.all()[0]
        self.url = "/questionnaire/entry/%s/section/%s/" % (self.questionnaire.id, self.section.id)

    def validate_fields(self):
        assert len(self.browser.find_by_name("form-0-response")) == 2
        assert self.browser.find_by_name("form-1-response")
        assert self.browser.find_by_id('cancel_button').text.strip() == "CANCEL"
        assert self.browser.find_by_id('save_draft_button').text.strip() == "SAVE"
        assert self.browser.find_by_id('submit_button').text.strip() == "SUBMIT"

    def validate_instructions(self, question):
        self.browser.click_link_by_text(" instructions")
        self.is_text_present(question.instructions)