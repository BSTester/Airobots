# -*- encoding=utf8 -*-

from airtest.core.api import *
from Core.runner import AirtestCase
from airtest.core.settings import Settings as ST
from TestCase.PageObjects.android_demo import DemoOP
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

class AndroidCase(AirtestCase):
    """Custom launcher."""

    @classmethod
    def setUpClass(cls):
        super(AndroidCase, cls).setUpClass()
        cls.android = DemoOP()

    def setUp(self):
        """Custom setup logic here."""
        # add var/function/class/.. to globals:
        # self.scope["add"] = lambda x: x+1
        # exec setup test script:
        # self.exec_other_script("setup.air")
        # set custom parameter in Settings:
        # ST.THRESHOLD = 0.75
        super(AndroidCase, self).setUp()

    def tearDown(self):
        """Custom tear down logic here."""
        # exec teardown script:
        # self.exec_other_script("teardown.air")
        super(AndroidCase, self).tearDown()

    @classmethod
    def tearDownClass(cls):
        super(AndroidCase, cls).tearDownClass()

    def test_heytea(self):
        self.android.wake_up_and_open_wechat()
        self.android.open_heytea()
        self.android.open_vip()
        nickname = poco(type="android.webkit.WebView", name="android.webkit.WebView").child('android.view.View').child('android.view.View').get_text()
        assert_equal(nickname, '阿白', '对比昵称是否正确')
        self.android.close_heytea()
        self.android.close_wechat()
