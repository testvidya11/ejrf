from lettuce.django import django_url
from nose.tools import assert_equals


class PageObject(object):
    url = None

    def __init__(self, browser):
        self.browser = browser

    def visit(self):
        self.browser.visit(django_url(self.url))

    def validate_url(self):
        assert self.browser.url == django_url(self.url)

    def fill(self, name, value):
        self.browser.fill(name, value)

    def is_text_present(self, text, status=True):
        assert_equals(status, self.browser.is_text_present(text))

    def submit(self):
        self.browser.find_by_css("form button").first.click()

    def click_link_by_text(self, text):
        self.browser.click_link_by_text(text)

    def click_by_css(self, css_selector):
        self.browser.find_by_css(css_selector).first.click()

    def click_link_by_partial_href(self, modal_id):
        self.browser.click_link_by_partial_href(modal_id)

    def click_link_by_href(self, modal_id):
        self.browser.click_link_by_href(modal_id)

    def click_by_name(self, name):
        self.browser.find_by_name(name).first.click()