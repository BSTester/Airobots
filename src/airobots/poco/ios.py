from poco.drivers.ios import iosPoco
from poco.utils import six
from airobots.core.api import snapshot, ST, try_log_screen, screen_attach, connect_device, device as current_device
from typing import List, Union
import allure
import os


class IOSUiautomation(iosPoco):
    def __init__(self, device=None, **kwargs):
        self.screenshot_each_action = True
        if kwargs.get('screenshot_each_action') is False:
            self.screenshot_each_action = False
        device = device or current_device()
        if not device:
            device = connect_device("iOS:///127.0.0.1:8100")
        self.device = device
        super(IOSUiautomation, self).__init__(device=device, **kwargs)

    def on_pre_action(self, action, ui, args):
        if self.screenshot_each_action:
            # airteset log用
            msg = repr(ui)
            if not isinstance(msg, six.text_type):
                msg = msg.decode('utf-8')
            screen = snapshot(msg=msg)
            filepath = os.path.join(ST.LOG_DIR, screen.get('screen'))
            with open(filepath, 'rb') as fp:
                allure.attach(fp.read(), '截图', allure.attachment_type.PNG)

    @allure.step
    def click(self, pos: Union[float, float]):
        ret = super(IOSUiautomation, self).click(pos)
        screen_attach()
        return ret

    @allure.step
    def swipe(self, p1: Union[float, float], p2: Union[float, float]=None, direction: Union[float, float]=None, duration: float=2.0):
        ret = super(IOSUiautomation, self).swipe(p1=p1, p2=p2, direction=direction, duration=duration)
        screen_attach()
        return ret

    @allure.step
    def long_click(self, pos: Union[float, float], duration: float=2.0):
        ret = super(IOSUiautomation, self).long_click(pos=pos, duration=duration)
        screen_attach()
        return ret

    @allure.step
    def scroll(self, direction: Union[List[float], str], percent: float=0.6, duration: float=2.0):
        ret = super(IOSUiautomation, self).scroll(direction=direction, percent=percent, duration=duration)
        screen_attach()
        return ret

    @allure.step
    def pinch(self, direction: str='in', percent: float=0.6, duration: float=2.0, dead_zone: float=0.1):
        ret = super(IOSUiautomation, self).pinch(direction=direction, percent=percent, duration=duration, dead_zone=dead_zone)
        screen_attach()
        return ret
