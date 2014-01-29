from questionnaire.features.pages.base import PageObject


class QuestionnairePage(PageObject):
    def __init__(self, browser, section):
        super(QuestionnairePage, self).__init__(browser)
        self.questionnaire = section.questionnaire
        self.section = section
        self.url = "/questionnaire/entry/%s/section/%s/" % (self.questionnaire.id, self.section.id)

    def validate_fields(self):
        assert self.browser.find_by_name("Number-0-response")
        assert self.browser.find_by_name("Number-1-response")
        assert self.browser.find_by_name("MultiChoice-0-response")
        assert self.browser.find_by_id('cancel_button').text.strip() == "CANCEL"
        assert self.browser.find_by_id('save_draft_button').text.strip() == "SAVE"
        assert self.browser.find_by_id('submit_button').text.strip() == "SUBMIT"

    def validate_instructions(self, question):
        self.browser.click_link_by_text(" instructions")
        self.is_text_present(question.instructions)