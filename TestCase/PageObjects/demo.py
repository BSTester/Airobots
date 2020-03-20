# -*- encoding=utf8 -*-

from airtest.core.api import *
from Core.runner import AirtestCase
from Core.Libs import AirSelenium
from airtest.core.settings import Settings as ST


class DemoOP(AirtestCase):
    """Demo page objects."""

    SEARCH_BOX = '//*[@id="kw"]'
    SEARCH_BUTTON = '//*[@id="su"]'
    LINK = '//div/h3/a[contains(string(), "{}")]'
    
    def __init__(self, driver):
        super(DemoOP, self).__init__()
        self.wd = driver

    def input_keywords(self, text):
        self.wd.input_text(self.SEARCH_BOX, text=text)

    def click_search_button(self):
        self.wd.click_button(self.SEARCH_BUTTON)

    def search(self, text):
        self.input_keywords(text=text)
        self.click_search_button()
        sleep(1)

    def search_and_click(self, text, click_text):
        self.search(text)
        self.wd.set_focus_to_element(self.LINK.format(click_text))
        self.wd.click_link(self.LINK.format(click_text))