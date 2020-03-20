# -*- encoding=utf8 -*-
__author__ = "BSTester"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from Core.runner import AirtestCase
import os

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

class DemoOP(AirtestCase):
    """Demo page objects."""
    def wake_up_and_open_wechat(self):
        wake()
        if poco("com.android.systemui:id/notification_stack_scroller").exists():
            poco("com.android.systemui:id/notification_stack_scroller").swipe([-0.0251, -0.4377])
        if poco("com.android.systemui:id/key8").exists():
            for _ in range(6):
                poco("com.android.systemui:id/key8").click()
            poco("com.android.systemui:id/key_enter_text").click()
        keyevent("HOME")
        start_app('com.tencent.mm')

    def open_heytea(self):
        poco(name="com.tencent.mm:id/civ", text='发现').click()
        poco(text="小程序").click()
        poco(text="喜茶GO").click()
        sleep(2)

    def open_vip(self):
        poco(name="com.tencent.mm:id/fwd", text="我的").click()
        touch(Template(os.path.join(os.path.dirname(__file__), r"tpl1584605281940.png"), record_pos=(0.281, -0.156), resolution=(1080, 2340)))
        sleep(2)

    def close_heytea(self):
        poco("com.tencent.mm:id/dc").click()
        poco(name="com.tencent.mm:id/fwd", text="点单").click()
        poco("关闭").click()

    def close_wechat(self):
        poco("com.tencent.mm:id/dn").click()
        poco(name="com.tencent.mm:id/civ", text='微信').click()
        stop_app('com.tencent.mm')
        keyevent("HOME")
