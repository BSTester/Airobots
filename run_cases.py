#!/usr/bin/env python3
# coding=utf8
__author__ = "BSTester"


import os
import sys
import argparse
from Core.runner import run_script
from airtest.cli.parser import runner_parser
from unittest import TestLoader
from airtest.report.report import main as report_main
from airtest.report.report import get_parger as report_parser
 

# 测试用例
# from TestCase.hello import CustomCase
from TestCase.android_hello import AndroidCase



def load_cases():
    suites = list()
    test_loader = TestLoader()
    # 加载用例
    suites.append(test_loader.loadTestsFromTestCase(AndroidCase))

    # 从用例类列表文件加载用例
    if os.path.isfile('be_run_cases.txt'):
        with open('be_run_cases.txt', 'r', encoding='utf8') as fp:
            be_run_tests_list = list()
            for test in fp.readlines():
                if test.strip():
                    be_run_tests_list.append(test.strip())
            if be_run_tests_list: suites = test_loader.loadTestsFromNames(be_run_tests_list)
    return suites


def reporter():
    ap = argparse.ArgumentParser()
    ap = report_parser(ap)
    ap.set_defaults(lang='zh', static_root=os.path.abspath(os.path.join('Core', 'Report')), outfile=os.path.join('Results', 'report.html'),
                    log_root='Results',  plugins=['poco.utils.airtest.report', 'Core.Report.report'])
    args = ap.parse_args(sys.argv)
    report_main(args)


if __name__ == '__main__':
    ap = runner_parser()
    ap.set_defaults(log='Results', recording=False, device=["Android:///"])
    args = ap.parse_args(sys.argv)
    run_script(args, load_cases())
    reporter()
