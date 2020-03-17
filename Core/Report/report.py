# -*- coding: utf-8 -*-
import os
import airtest.report.report as report

LOGDIR = "log"

old_trans_screen = report.LogToHtml._translate_screen
old_trans_desc = report.LogToHtml._translate_desc
old_trans_code = report.LogToHtml._translate_code

screen_func = ["find_element_by_xpath", "find_element_by_id", "find_element_by_name", "assert_exist",
               "back", "forward", "switch_to_new_tab", "switch_to_previous_tab", "get", "find_element",
               "click", "send_keys", "click_element", "click_link", "click_image", "click_button", "input_text", "input_password", "double_click_element", 
               "open_context_menu", "mouse_up", "mouse_down", "drag_and_drop_by_offset", "mouse_over", "mouse_out", "drag_and_drop", "go_to"]

second_screen_func = ["click", "send_keys"]
other_func = ['page_should_contain', 'page_should_not_contain']

def new_trans_screen(self, step, code):
    trans = old_trans_screen(self, step, code)
    if "name" in step['data'] and step['data']["name"] in screen_func:
        screen = {
            "src": None,
            "rect": [],
            "pos": [],
            "vector": [],
            "confidence": None,
        }

        src = ""
        if step["data"]["name"] in second_screen_func:
            res = step["data"]['ret']
            src = res["screen"]
            if "pos" in res:
                screen["pos"] = res["pos"]

        for item in step["__children__"]:
            if item["data"]["name"] == "_gen_screen_log":
                res = item["data"]['ret']
                src = res["screen"]
                if "pos" in res:
                    screen["pos"] = res["pos"]
                break

        if self.export_dir and src:
            src = os.path.join(LOGDIR, src)
        screen["src"] = src

        return screen
    else:
        return trans

def new_translate_desc(self, step, code):
    trans = old_trans_desc(self, step, code)
    if "name" in step['data'] and (step['data']["name"] in screen_func or step["data"]["name"] in other_func):
        name = step["data"]["name"]
        args = {i["key"]: i["value"] for i in code["args"]}
        desc = {
            "find_element_by_xpath": lambda: u"Find element by xpath: %s" % args.get("xpath"),
            "find_element_by_id": lambda: u"Find element by id: %s" % args.get("id"),
            "find_element_by_name": lambda: u"Find element by name: %s" % args.get("name"),
            "find_element": lambda: u"Find element by locator: %s" % args.get("locator"),
            "assert_exist": u"Assert element exists.",
            "click": u"Click the element that been found.",
            "click_element": u"Click the element that been found.",
            "click_link": u"Click the link that been found.",
            "click_image": u"Click the image that been found.",
            "click_button": u"Click the button that been found.",
            "double_click_element": u"Double click the element that been found.",
            "send_keys": u"Send some text and keyboard event to the element that been found.",
            "input_text": u"Send some text and keyboard event to the element that been found.",
            "input_password": u"Send some text and keyboard event to the element that been found.",
            "get": lambda: u"Get the web address: %s" % args.get("address"),
            "go_to": lambda: u"Get the web address: %s" % args.get("url"),
            "switch_to_last_window": u"Switch to the last tab.",
            "switch_to_latest_window": u"Switch to the new tab.",
            "back": u"Back to the last page.",
            "forward": u"Forward to the next page.",
            "open_context_menu": u"Open context menu.",
            "mouse_up": u"Mouse up.",
            "mouse_down": u"Mouse down.",
            "mouse_out": u"Mouse out.",
            "mouse_over": u"Mouse over.",
            "drag_and_drop": u"Drag and drop.",
            "drag_and_drop_by_offset": u"Drag and drop by offset(%s,%s)." % (args.get('xoffset', ''), args.get('yoffset', '')),
            "page_should_contain": u"Page should have contained text: \"%s\"." % args.get('text', ''),
            "page_should_not_contain": u"Page should not have contained text: \"%s\"." % args.get('text', ''),
            "snapshot": u"Snopshot current page."
        }

        desc_zh = {
            "find_element_by_xpath": lambda: u"寻找指定页面元素: \"%s\"" % args.get("xpath"),
            "find_element_by_id": lambda: u"寻找指定页面元素: \"%s\"" % args.get("id"),
            "find_element_by_name": lambda: u"寻找指定页面元素: \"%s\"" % args.get("name"),
            "find_element": lambda: u"寻找指定页面元素: \"%s\"" % args.get("locator"),
            "assert_exist": u"断言页面元素存在.",
            "click": u"点击找到的页面元素.",
            "click_element": u"点击找到的页面元素.",
            "click_link": u"点击找到的页面链接.",
            "click_image": u"点击找到的页面图片.",
            "click_button": u"点击找到的页面按钮.",
            "double_click_element": u"双击找到的页面元素.",
            "send_keys": u"传送文本\"%s\"到选中文本框." % (args.get("text", "")),
            "input_text": u"传送文本\"%s\"到选中文本框." % (args.get("text", "")),
            "input_password": u"传送文本\"%s\"到选中密码文本框." % (args.get("password", "")),
            "get": lambda: u"访问网络地址: %s" % args.get("address"),
            "go_to": lambda: u"访问网络地址: %s" % args.get("url"),
            "switch_to_last_window": u"切换到上一个标签页.",
            "switch_to_latest_window": u"切换到最新标签页.",
            "back": u"后退到上一个页面.",
            "forward": u"前进到下一个页面.",
            "open_context_menu": u"打开右键菜单.",
            "mouse_up": u"在找到的页面元素上松开鼠标左键.",
            "mouse_down": u"在找到的页面元素上按下鼠标左键.",
            "mouse_out": u"在找到的页面元素上移开光标.",
            "mouse_over": u"移动光标到找到的页面元素上.",
            "drag_and_drop": u"拖动一个页面元素到另一个页面元素上.",
            "drag_and_drop_by_offset": u"在找到的页面元素上拖动到指定坐标(%s,%s)." % (args.get('xoffset', ''), args.get('yoffset', '')),
            "page_should_contain": u"页面上应该存在文本\"%s\"." % args.get('text', ''),
            "page_should_not_contain": u"页面上不应该存在文本\"%s\"." % args.get('text', ''),
            "snapshot": u"截取当前页面."
        }

        if self.lang == 'zh':
            desc = desc_zh
        ret = desc.get(name)
        if callable(ret):
            ret = ret()
        return ret
    else:
        return trans

def new_translate_code(self, step):
    trans = old_trans_code(self, step)
    if trans:
        for idx, item in enumerate(trans["args"]):
            if item["key"] == "self":
                trans["args"].pop(idx)
    return trans


report.LogToHtml._translate_screen = new_trans_screen
report.LogToHtml._translate_desc = new_translate_desc
report.LogToHtml._translate_code = new_translate_code

