import os
import sys
import time
import inspect
import traceback
import functools
from selenium import webdriver
from SeleniumLibrary.base.robotlibcore import PY2
from robot.libraries.BuiltIn import RobotNotRunningError
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import (AlertKeywords,
                                      BrowserManagementKeywords,
                                      CookieKeywords,
                                      ElementKeywords,
                                      FormElementKeywords,
                                      FrameKeywords,
                                      JavaScriptKeywords,
                                      RunOnFailureKeywords,
                                      ScreenshotKeywords,
                                      SelectElementKeywords,
                                      TableElementKeywords,
                                      WaitingKeywords,
                                      WindowKeywords)
from airtest import aircv
from airtest_selenium.proxy import Element
from airtest.core.helper import G
from airtest_selenium.proxy import WebChrome


def Logwrap(f, logger):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        m = inspect.getcallargs(f, *args, **kwargs)
        m['self'] = str(m.get('self'))
        fndata = {'name': f.__name__, 'call_args': m, 'start_time': start}
        logger.running_stack.append(fndata)
        try:
            res = f(*args, **kwargs)
        except Exception as e:
            data = {"traceback": traceback.format_exc(), "end_time": time.time()}
            fndata.update(data)
            raise
        else:
            fndata.update({'ret': res, "end_time": time.time()})
        finally:
            logger.log('function', fndata)
            logger.running_stack.pop()
        return res
    return wrapper


def logwrap(f):
    return Logwrap(f, G.LOGGER)


class AirSelenium(
    AlertKeywords,
    BrowserManagementKeywords,
    CookieKeywords,
    ElementKeywords,
    FormElementKeywords,
    FrameKeywords,
    JavaScriptKeywords,
    RunOnFailureKeywords,
    ScreenshotKeywords,
    SelectElementKeywords,
    TableElementKeywords,
    WaitingKeywords,
    WindowKeywords):
    
    def __init__(self, screenshot_root_directory=os.path.join('Results', 'log'), web_driver=WebChrome, alias=None, device=None, headless=None, executable_path="chromedriver"):
        ctx = SeleniumLibrary(screenshot_root_directory=screenshot_root_directory)
        if web_driver and inspect.isclass(web_driver) and web_driver.__name__ == 'WebChrome': 
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            if headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            if device:
                mobile_emulation = {'deviceName': device}
                chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
            ctx.register_driver(web_driver(executable_path=executable_path, chrome_options=chrome_options), alias)
        self.screenshot_directory = ctx.screenshot_root_directory
        super(AirSelenium, self).__init__(ctx)
    
    @logwrap
    def find_element(self, locator, tag=None, required=True, parent=None):
        web_element = super(AirSelenium, self).find_element(locator=locator, tag=tag, required=required, parent=parent)
        log_res=self._gen_screen_log(web_element)
        return Element(web_element, log_res)

    @logwrap
    def click_element(self, locator, modifier=False, action_chain=False):
        super(AirSelenium, self).click_element(locator=locator, modifier=modifier, action_chain=action_chain)

    @logwrap
    def click_link(self, locator, modifier=False):
        super(AirSelenium, self).click_link(locator=locator, modifier=modifier)

    @logwrap
    def click_image(self, locator, modifier=False):
        super(AirSelenium, self).click_image(locator=locator, modifier=modifier)

    @logwrap
    def click_button(self, locator, modifier=False):
        super(AirSelenium, self).click_button(locator=locator, modifier=modifier)

    @logwrap
    def input_text(self, locator, text, clear=True):
        super(AirSelenium, self).input_text(locator=locator, text=text, clear=clear)

    @logwrap
    def input_password(self, locator, password, clear=True):
        super(AirSelenium, self).input_password(locator=locator, password=password, clear=clear)

    @logwrap
    def double_click_element(self, locator):
        super(AirSelenium, self).double_click_element(locator=locator)

    @logwrap
    def page_should_contain(self, text, loglevel='TRACE'):
        super(AirSelenium, self).page_should_contain(text=text, loglevel=loglevel)

    @logwrap
    def page_should_not_contain(self, text, loglevel='TRACE'):
        super(AirSelenium, self).page_should_not_contain(text=text, loglevel=loglevel)

    @logwrap
    def open_context_menu(self, locator):
        super(AirSelenium, self).open_context_menu(locator=locator)

    @logwrap
    def mouse_up(self, locator):
        super(AirSelenium, self).mouse_up(locator=locator)
    
    @logwrap
    def mouse_down(self, locator):
        super(AirSelenium, self).mouse_down(locator=locator)

    @logwrap
    def mouse_over(self, locator):
        super(AirSelenium, self).mouse_over(locator=locator)

    @logwrap
    def mouse_out(self, locator):
        super(AirSelenium, self).mouse_out(locator=locator)

    @logwrap
    def drag_and_drop(self, locator, target):
        super(AirSelenium, self).drag_and_drop(locator=locator, target=target)

    @logwrap
    def drag_and_drop_by_offset(self, locator, xoffset, yoffset):
        super(AirSelenium, self).drag_and_drop_by_offset(locator=locator, xoffset=xoffset, yoffset=yoffset)

    @logwrap
    def go_to(self, url):
        super(AirSelenium, self).go_to(url=url)

    def screenshot(self, file_path=None):
        if file_path:
            self.capture_page_screenshot(file_path)
        else:
            if not self.screenshot_directory:
                file_path = "temp.jpg"
            else:
                file_path = os.path.join('', "temp.jpg")
            self.capture_page_screenshot(file_path)
            screen = aircv.imread(file_path)
            return screen

    @logwrap
    def _gen_screen_log(self, element=None, filename=None,):
        if self.screenshot_directory is None:
            return None
        if filename:
            self.screenshot(filename)
        jpg_file_name=str(int(time.time())) + '.jpg'
        jpg_path=os.path.join('', jpg_file_name)
        print("this is jpg path:", jpg_path)
        self.screenshot(jpg_path)
        saved={"screen": jpg_file_name}
        if element:
            size=element.size
            location=element.location
            x=size['width'] / 2 + location['x']
            y=size['height'] / 2 + location['y']
            if "darwin" in sys.platform:
                x, y=x * 2, y * 2
            saved.update({"pos": [[x, y]]})
        return saved

    @property
    def log_dir(self):
        try:
            if os.path.isdir(self.screenshot_directory):
                return os.path.abspath(self.screenshot_directory)
            else:
                os.makedirs(self.screenshot_directory)
                return os.path.abspath(self.screenshot_directory)
        except RobotNotRunningError:
            return os.getcwd() if PY2 else os.getcwd()

    def open_browser(self, url, browser='Chrome', alias=None, remote_url=None,
            desired_capabilities=None, ff_profile_dir=None, device=None, maximize_browser=True):
        """
        启动浏览器类型，可选：Firefox、Chrome、Headless, 可模拟移动设备
        """
        if browser not in ['Firefox', 'Chrome', 'Headless']:
            raise Exception('浏览器类型不对, 仅可选: Firefox, Chrome, Headless')
        chrome_options = webdriver.ChromeOptions()
        if browser == 'Headless':
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options = chrome_options.to_capabilities()
        elif device and browser == 'Chrome':
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            mobile_emulation = {'deviceName': device}
            chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
            chrome_options = chrome_options.to_capabilities()
        elif browser == 'Chrome':
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options = chrome_options.to_capabilities()
        else:
            chrome_options = None
        if remote_url:
            browser = self.create_webdriver(driver_name=browser, alias=alias, command_executor=remote_url, desired_capabilities=desired_capabilities or chrome_options)
        else:
            browser = self.create_webdriver(driver_name=browser, alias=alias, desired_capabilities=desired_capabilities or chrome_options)
        self.go_to(url=url)
        maximize_browser and self.maximize_browser_window()
        return browser
