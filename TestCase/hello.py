# -*- encoding=utf8 -*-

from airtest.core.api import *
from Core.runner import AirtestCase
from Core.Libs import AirSelenium
from airtest.core.settings import Settings as ST


class CustomCase(AirtestCase):
    """Custom launcher."""

    def setUp(self):
        """Custom setup logic here."""

        # # add var/function/class/.. to globals:
        # self.scope["add"] = lambda x: x+1

        # # exec setup test script:
        # self.exec_other_script("setup.air")

        # # set custom parameter in Settings:
        # ST.THRESHOLD = 0.75

        super(CustomCase, self).setUp()
        self.wd = AirSelenium()
        self.wd.set_browser_implicit_wait(20)

    def tearDown(self):
        """Custom tear down logic here."""
        # # exec teardown script:
        # self.exec_other_script("teardown.air")

        super(CustomCase, self).tearDown()
        self.wd.close_browser()

    def test_chrome(self):
        self.wd.go_to('https://www.baidu.com')
        self.wd.maximize_browser_window()
        self.wd.input_text('//*[@id="kw"]', '软件测试')
        self.wd.click_element('//*[@id="su"]')
        time.sleep(2)
        self.wd.page_should_contain('测试')
        self.wd.driver.get('https://www.qq.com')
        self.wd.click_link('新闻')
        self.wd.switch_window('NEW')
        title = self.wd.get_title()
        assert_equal(title, '新闻中心-腾讯网', '页面标题错误')



