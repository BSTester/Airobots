# -*- coding: utf-8 -*-
"""
This module contains the Airtest Core APIs.
"""
import os
import time

from six.moves.urllib.parse import parse_qsl, urlparse

from airtest.core.cv import Template, loop_find, try_log_screen
from airtest.core.error import TargetNotFoundError
from airtest.core.settings import Settings as ST
from airtest.utils.compat import script_log_dir
from airtest.core.helper import (G, delay_after_operation, import_device_cls,
                                 logwrap, set_logdir, using, log)

from airtest.core.api import init_device, connect_device, device, set_current, auto_setup
from airtest.core.api import shell as air_shell
from airtest.core.api import start_app as air_start_app
from airtest.core.api import stop_app as air_stop_app
from airtest.core.api import clear_app as air_clear_app
from airtest.core.api import install as air_install
from airtest.core.api import uninstall as air_uninstall
from airtest.core.api import snapshot as air_snapshot
from airtest.core.api import wake as air_wake
from airtest.core.api import home as air_home
from airtest.core.api import touch as air_touch
from airtest.core.api import double_click as air_double_click
from airtest.core.api import swipe as air_swipe
from airtest.core.api import pinch as air_pinch
from airtest.core.api import keyevent as air_keyevent
from airtest.core.api import text as air_text
from airtest.core.api import sleep as air_sleep
from airtest.core.api import wait as air_wait
from airtest.core.api import exists as air_exists
from airtest.core.api import find_all as air_find_all
from airtest.core.api import assert_exists as air_assert_exists
from airtest.core.api import assert_not_exists as air_assert_not_exists
from airtest.core.api import assert_equal as air_assert_equal
from airtest.core.api import assert_not_equal as air_assert_not_equal
import allure


def screen_attach():
    screen = try_log_screen()
    filepath = os.path.join(ST.LOG_DIR, screen.get('screen'))
    with open(filepath, 'rb') as fp:
        allure.attach(fp.read(), '截图', allure.attachment_type.JPG)

@allure.step
def shell(cmd):
    return air_shell(cmd)


@allure.step
def start_app(package, activity=None):
    air_start_app(package, activity)


@allure.step
def stop_app(package):
    air_stop_app(package)


@allure.step
def clear_app(package):
    air_clear_app(package)


@allure.step
def install(filepath, **kwargs):
    return air_install(filepath, **kwargs)


@allure.step
def uninstall(package):
    return air_uninstall(package)


@allure.step
def snapshot(filename=None, msg="", quality=None, max_size=None):
    return air_snapshot(filename=filename, msg=msg, quality=quality, max_size=max_size)


@allure.step
def wake():
    air_wake()


@allure.step
def home():
    air_home()


@allure.step
def touch(v, times=1, **kwargs):
    pos = air_touch(v, times=times, **kwargs)
    screen_attach()
    return pos

click = touch  # click is alias of touch


@allure.step
def double_click(v):
    pos = air_double_click(v)
    screen_attach()
    return pos


@allure.step
def swipe(v1, v2=None, vector=None, **kwargs):
    pos = air_swipe(v1, v2=v2, vector=vector, **kwargs)
    screen_attach()
    return pos


@allure.step
def pinch(in_or_out='in', center=None, percent=0.5):
    air_pinch(in_or_out=in_or_out, center=center, percent=percent)
    screen_attach()


@allure.step
def keyevent(keyname, **kwargs):
    air_keyevent(keyname, **kwargs)


@allure.step
def text(text, enter=True, **kwargs):
    air_text(text, enter=enter, **kwargs)
    screen_attach()


@allure.step
def sleep(secs=1.0):
    air_sleep(secs)


@allure.step
def wait(v, timeout=None, interval=0.5, intervalfunc=None):
    return air_wait(v, timeout=timeout, interval=interval, intervalfunc=intervalfunc)


@allure.step
def exists(v):
    return air_exists(v)


@allure.step
def find_all(v):
    return air_find_all(v)


"""
Assertions
"""


@allure.step
def assert_exists(v, msg=""):
    return air_assert_exists(v, msg=msg)


@allure.step
def assert_not_exists(v, msg=""):
    return air_assert_not_exists(v, msg=msg)


@allure.step
def assert_equal(first, second, msg=""):
    return air_assert_equal(first, second, msg=msg)

@allure.step
def assert_not_equal(first, second, msg=""):
    return air_assert_not_equal(first, second, msg=msg)