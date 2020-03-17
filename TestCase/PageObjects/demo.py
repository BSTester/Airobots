# -*- encoding=utf8 -*-

from airtest.core.api import *
from Core.runner import AirtestCase
from Core.Libs import AirSelenium
from airtest.core.settings import Settings as ST
import time


class DemoOP(AirtestCase):
    """Demo page objects."""
    
    def __init__(self, driver):
        super(DemoOP, self).__init__()
        self.wd = driver

    def input_keywords(self, text):
        self.wd.input_text('//*[@id="kw"]', text=text)

    def click_search_button(self):
        self.wd.click_button('//*[@id="su"]')

    def search(self, text):
        self.input_keywords(text=text)
        self.click_search_button()
        time.sleep(1)

    def search_and_click(self, text):
        self.search(text)
        self.wd.click_link('//*[@id="1"]/h3/a')