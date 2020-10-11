# -*- encoding=utf8 -*-

from airtest.core.api import *
from Core.runner import AirtestCase
from Core.Libs import AirSelenium
from airtest.core.settings import Settings as ST
from TestCase.PageObjects.demo import DemoOP


class CustomCase(AirtestCase):
    """Custom launcher."""

    @classmethod
    def setUpClass(cls):
        super(CustomCase, cls).setUpClass()
        cls.wd = AirSelenium()
        cls.wd.set_browser_implicit_wait(20)
        cls.baidu = DemoOP(driver=cls.wd)

    def setUp(self):
        """Custom setup logic here."""
        # add var/function/class/.. to globals:
        # self.scope["add"] = lambda x: x+1
        # exec setup test script:
        # self.exec_other_script("setup.air")
        # set custom parameter in Settings:
        # ST.THRESHOLD = 0.75
        super(CustomCase, self).setUp()

    def tearDown(self):
        """Custom tear down logic here."""
        # exec teardown script:
        # self.exec_other_script("teardown.air")
        super(CustomCase, self).tearDown()

    @classmethod
    def tearDownClass(cls):
        super(CustomCase, cls).tearDownClass()
        cls.wd.close_browser()

    def test_baidu(self):
        # 使用RobotFrameWork-SeleniumLibrary方法
        self.wd.go_to('https://www.baidu.com')
        self.wd.maximize_browser_window()
        self.baidu.search_and_click('软件测试', '百度百科')
        self.wd.switch_window('NEW')
        self.wd.page_should_contain('百度百科')
        # 可混合使用selenium原生方法
        self.wd.driver.get('https://www.qq.com')
        self.wd.click_link('新闻')
        self.wd.switch_window('NEW')
        title = self.wd.get_title()
        assert_equal(title, '新闻中心-腾讯网', '对比页面标题')

    def test_baidu_other(self):
        # 使用RobotFrameWork-SeleniumLibrary方法
        self.wd.go_to('https://www.baidu.com')
        self.wd.maximize_browser_window()
        self.baidu.search_and_click('软件测试', '百度百科')
        self.wd.switch_window('NEW')
        self.wd.page_should_contain('百度百科')
        # 可混合使用selenium原生方法
        self.wd.driver.get('https://www.qq.com')
        self.wd.click_link('新闻')
        self.wd.switch_window('NEW')
        title = self.wd.get_title()
        assert_equal(title, '新闻中心-腾讯网', '对比页面标题')
