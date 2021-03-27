from poco.drivers.ios import iosPoco
from poco.utils import six
from airobots.core.api import ST, screen_attach, connect_device, device as current_device
from typing import List, Union
import allure
import os


class IOSUiautomation(iosPoco):
    def __init__(self, device=None, screenshot_each_action=True, **kwargs):
        self.screenshot_each_action = screenshot_each_action
        device = device or current_device()
        if not device:
            device = connect_device("iOS:///127.0.0.1:8100")
        self.device = device
        super(IOSUiautomation, self).__init__(device=device, **kwargs)

    @allure.step
    def click(self, pos: Union[float, float]):
        ret = super(IOSUiautomation, self).click(pos)
        if self.screenshot_each_action: screen_attach()
        return ret

    @allure.step
    def swipe(self, p1: Union[float, float], p2: Union[float, float]=None, direction: Union[float, float]=None, duration: float=2.0):
        ret = super(IOSUiautomation, self).swipe(p1=p1, p2=p2, direction=direction, duration=duration)
        if self.screenshot_each_action: screen_attach()
        return ret

    @allure.step
    def long_click(self, pos: Union[float, float], duration: float=2.0):
        ret = super(IOSUiautomation, self).long_click(pos=pos, duration=duration)
        if self.screenshot_each_action: screen_attach()
        return ret

    @allure.step
    def scroll(self, direction: Union[List[float], str], percent: float=0.6, duration: float=2.0):
        ret = super(IOSUiautomation, self).scroll(direction=direction, percent=percent, duration=duration)
        if self.screenshot_each_action: screen_attach()
        return ret

    @allure.step
    def pinch(self, direction: str='in', percent: float=0.6, duration: float=2.0, dead_zone: float=0.1):
        ret = super(IOSUiautomation, self).pinch(direction=direction, percent=percent, duration=duration, dead_zone=dead_zone)
        if self.screenshot_each_action: screen_attach()
        return ret
