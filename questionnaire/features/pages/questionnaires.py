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
        self.click_by_css("#question-%d-instructions" % question.id)
        self.is_text_present(question.instructions)

    def validate_alert_success(self):
        self.is_text_present("Draft saved")
        self.is_element_present_by_css(".alert-success")

    def validate_alert_error(self):
        self.is_text_present("Draft NOT saved. See errors below")
        self.is_element_present_by_css(".alert-danger")