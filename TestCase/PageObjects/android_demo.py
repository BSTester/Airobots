# -*- encoding=utf8 -*-
__author__ = "BSTester"

from airtest.core.api import *
from unittest import TestCase
import os


class DemoOP(TestCase):
    def __init__(self, driver):
        super(DemoOP, self).__init__()
        self.poco = driver

    """Demo page objects."""
    def wake_up_and_open_wechat(self):
        wake()
        if self.poco("com.android.systemui:id/notification_stack_scroller").exists():
            self.poco("com.android.systemui:id/notification_stack_scroller").swipe([-0.0251, -0.4377])
        if self.poco("com.android.systemui:id/key8").exists():
            for _ in range(6):
                self.poco("com.android.systemui:id/key8").click()
            self.poco("com.android.systemui:id/key_enter_text").click()
        keyevent("HOME")
        start_app('com.tencent.mm')

    def open_heytea(self):
        self.poco(name="com.tencent.mm:id/civ", text='发现').click()
        self.poco(text="小程序").click()
        self.poco(text="喜茶GO").click()
        sleep(2)

    def open_vip(self):
        self.poco(name="com.tencent.mm:id/fwd", text="我的").click()
        touch(Template(os.path.join(os.path.dirname(__file__), r"tpl1584605281940.png"), record_pos=(0.281, -0.156), resolution=(1080, 2340)))
        sleep(2)

    def close_heytea(self):
        self.poco("com.tencent.mm:id/dc").click()
        self.poco(name="com.tencent.mm:id/fwd", text="点单").click()
        self.poco("关闭").click()

    def close_wechat(self):
        self.poco("com.tencent.mm:id/dn").click()
        self.poco(name="com.tencent.mm:id/civ", text='微信').click()
        stop_app('com.tencent.mm')
        keyevent("HOME")
