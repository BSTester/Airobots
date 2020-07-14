# -*- coding: utf8 -*-
# Author: Penn
# Todo: 数据接口测试,与数据库查询结果作对比

import http.client as httplib
from urllib.parse import urlencode
import requests
import json
import pymysql
import os
import time
import difflib
import ast


class DataDiffLibrary(object):
    def __init__(self, result_folder='Results'):
        """
        初始化headers
        """
        self.headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                       ' Chrome/50.0.2652.2 Safari/537.36')}
        self.result_folder = result_folder

    def __parse_none_to_empty_as_dict(self, has_none_dict):
        if isinstance(has_none_dict, dict):
            for key in has_none_dict:
                if has_none_dict[key] is None:
                    has_none_dict[key] = ''
                elif isinstance(has_none_dict[key], dict) or isinstance(has_none_dict[key], list):
                    has_none_dict[key] = self.__parse_none_to_empty_as_dict(has_none_dict[key])
        elif isinstance(has_none_dict, list):
            for row in has_none_dict:
                row = self.__parse_none_to_empty_as_dict(row)
        return has_none_dict

    def __interface_test(self, url, method, body, cookie='',content_type='JSON', auto_redirect=False):
        """
        接口测试
        | :param url: 请求的链接地址
        | :param method: 请求方法
        | :param body: 请求数据
        | :param auto_redirect: 是否重定向跟随
        | :param cookie: 请求时带的cookie, 默认为空
        | :return: 服务器响应状态码, 服务器返回内容
        """
        if not isinstance(body, dict):
            try:
                body = json.loads(str(body))
            except:
                body = str(body)
        urls = self.__urlsplit(url)
        self.headers['Host'] = '{}:{}'.format(urls['host'], urls['port'])
        self.headers['Origin'] = 'http://{}:{}'.format(urls['host'], urls['port'])
        self.headers['Referer'] = 'http://{}:{}{}'.format(urls['host'], urls['port'], urls['path'])
        self.headers['Cookie'] = cookie
        if content_type == 'FORM':
            self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        else:
            self.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            self.headers['Content-Type'] = 'application/json'
        # for key in body.keys():
        #     if isinstance(body[key], unicode):
        #         body[key] = body[key].encode('utf8')
        # conn = httplib.HTTPConnection(host=urls['host'], port=urls['port'])
        try:
            if method == 'GET':
                if isinstance(body, dict):
                    body = urlencode(body)
                resp = requests.get(url='{}?{}'.format(url, body), headers=self.headers, allow_redirects=auto_redirect)
            elif method == 'POST':
                if isinstance(body, dict) and content_type == 'JSON':
                    body = json.dumps(body, encoding='utf8')
                elif isinstance(body, dict) and content_type == 'FORM':
                    body = urlencode(body)
                resp = requests.post(url=url, data=body, headers=self.headers, allow_redirects=auto_redirect)
            else:
                print(u'暂不支持其他请求类型')
            status = resp.status_code
            reason = resp.reason
            content = resp.text
            resp_headers = resp.headers
        except Exception as e:
            print('[ERROR] Interface test failed! => {}'.format(e))
            status = 5001
            content = e
            resp_headers = {'Set-Cookie': ''}
        return status, content, resp_headers

    def __urlsplit(self, url):
        """
        切割url
        | :param url: url链接
        | :return: 切割url后的字典 {'scheme': scheme, 'host': host, 'port': port, 'path': path, 'query': query, 'fragment': fragment}
        """
        url = httplib.urlsplit(url)
        scheme = url[0]
        netloc = url[1].split(':')
        if len(netloc) == 2:
            host = netloc[0]
            port = int(netloc[1])
        else:
            host = url[1]
            if scheme == 'https':
                port = 443
            else:
                port = 80
        path = url[2]
        query = url[3]
        fragment = url[4]
        return {'scheme': scheme, 'host': host, 'port': port, 'path': path, 'query': query, 'fragment': fragment}

    def login_interface(self, url, body):
        """
        登录接口, 获取session  
        | :param url: 登录接口地址, http协议
        | :param body: 包含用户名和密码的请求数据, 格式如 {"username": "user", "password": "passwd"}, 视具体接口而定
        | :return: session
        """
        status, content, headers = self.__interface_test(url=url, method='POST', body=body, content_type='FORM')
        if status not in (301, 302):
            assert False, u'登录失败! => {}'.format(content)
        return headers['Set-Cookie']

    def get_interface_data(self, url, method, body, cookie, key='rows', content_type='JSON', file=True):
        """
        获取接口数据
        | :param url: 接口地址, http协议
        | :param method: 请求方法
        | :param body: 请求数据
        | :param cookie: cookie
        | :param key: 获取服务器返回的json数据中指定key的值, 默认取所有
        | :param content_type: 提交的数据类型, JSON或FORM, POST操作时选填, 默认为JSON
        | :param file: 是否保存为文件, 默认返回保存文件路径, 否则直接返回接口数据
        | :return: 服务器返回的指定key的数据
        """
        status, content, headers = self.__interface_test(url=url, method=method, body=body, cookie=cookie, content_type=content_type, auto_redirect=True)
        try:
            if status != 200:
                assert False, u'获取接口数据失败! => {}'.format(content)
            elif key != '' and content.find(key) > 0:
                source_content = json.loads(content, parse_int=float)[key]
                content = source_content
            else:
                content = json.loads(content, parse_int=float)
        except Exception as e:
            print(u'{} 将返回原始接口数据!'.format(e))
            content = content
        if file:
            result_folder = os.path.normpath(os.path.abspath(self.result_folder))
            result_folder = os.path.normpath('{}/{}'.format(result_folder, time.strftime('%Y%m%d')))
            if not os.path.isdir(result_folder):
                os.makedirs(result_folder)
            now = '{}.{}'.format(time.strftime('%H%M%S'), repr(time.time()).split('.')[1])
            source_file = os.path.normpath('{}/source_{}_interface.txt'.format(result_folder, now))
            with open(source_file, 'a', encoding='utf8') as fp:
                if content is not None and isinstance(content, list):
                    for row in content:
                        row = json.dumps(self.__parse_none_to_empty_as_dict(row), sort_keys=True, ensure_ascii=False)
                        fp.writelines('{}\n'.format(row))
                else:
                    fp.writelines(content)
            return source_file, len(content)   
        else:
            return content, len(content)   

    def get_database_data(self, host, port, database, username, password, sql_file, param={}, add_data=[], file=True):
        """
        获取数据库数据
        | :param host: mysql地址
        | :param port: mysql端口
        | :param database: mysql数据库名
        | :param username: 用户名
        | :param password: 密码
        | :param sql_file: 要执行的sql语句文件路径
        | :param param: 参数字典
        | :param file: 是否保存为文件, 默认返回保存文件路径, 否则直接返回接口数据
        | :param add_data: 叠加数据, 拼接两次查询结果, 留空则不拼接
        | :return: json格式的查询结果
        """
        if isinstance(add_data, str) and os.path.isfile(add_data):
            file = True
        elif isinstance(add_data, list) and len(add_data) > 0:
            file = False
        if file:
            result_folder = os.path.normpath(os.path.abspath(self.result_folder))
            result_folder = os.path.normpath('{}/{}'.format(result_folder, time.strftime('%Y%m%d')))
            if not os.path.isdir(result_folder):
                os.makedirs(result_folder)
            now = '{}.{}'.format(time.strftime('%H%M%S'), repr(time.time()).split('.')[1])
            source_file = os.path.normpath('{}/source_{}_database.txt'.format(result_folder, now))
        if not isinstance(param, dict):
            try:
                param = json.loads(str(param))
            except:
                param = dict(param)
        # for key in param.keys():
        #     if isinstance(param[key], unicode):
        #         param[key] = param[key].encode('utf8')
        if not os.path.isfile(sql_file):
            print(u'SQL文件 {} 不存在, 尝试作为sql语句执行!'.format(sql_file))
            sql = sql_file.replace("\r", " ").replace("\n", " ")
        else:
            with open(sql_file, 'r', encoding='utf8') as fp:
                sql = fp.read().format(**param)
        conn = self.__connect_mysql(host=host, port=port, database=database,
                                    username=username, password=password)
        result = self.__run_sql(conn=conn, sql=sql, mode='dict')
        conn.close()
        if isinstance(add_data, str) and os.path.isfile(add_data):
            source_file = add_data
        elif isinstance(add_data, list) and len(add_data) > 0:
            result = add_data + result
        data = {'rows':result}
        if file:
            result = json.loads(json.dumps(data, sort_keys=True), encoding='utf8', parse_int=float)['rows']
            with open(source_file, 'a', encoding='utf8') as fp:
                if result is not None:
                    for row in result:
                        row = json.dumps(self.__parse_none_to_empty_as_dict(row), sort_keys=True, ensure_ascii=False)
                        fp.writelines('{}\n'.format(row))
            return source_file, len(result)  
        else:
            result = json.loads(json.dumps(data, sort_keys=True), encoding='utf8', parse_int=float)['rows']
            return result, len(result)  

    def __run_sql(self, conn, sql, mode='tuple'):
        """
        执行mysql语句
        | :param conn: mysql数据库对象
        | :param sql: 要执行的sql语句
        | :param mode: 返回的结果集类型, 默认tuple:元组, dict:字典
        | :return: 查询结果
        """
        try:
            if mode == 'tuple':
                cur = conn.cursor()
                zero = ()
            else:
                cur = conn.cursor(pymysql.cursors.DictCursor)
                zero = []
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
        except pymysql.DataError as e:
            assert False, u'执行SQL语句出错! => {}'.format(e)
        if len(result) == 0:
            result = zero
        return result

    def __connect_mysql(self, host, port, database, username, password, charset='utf8'):
        """
        连接mysql数据库
        | :param host: mysql地址
        | :param port: mysql端口
        | :param database: mysql数据库名
        | :param username: 用户名
        | :param password: 密码
        | :param charset: 数据库编码类型
        | :return: mysql对象
        """
        try:
            conv = pymysql.converters.conversions.copy()
            conv[0] = float
            conv[10] = str
            conv[12] = str
            conv[246] = float
            conn = pymysql.connect(host=host, port=port, db=database,
                                   user=username, passwd=password, charset=charset, conv=conv)
        except pymysql.MySQLError as e:
            assert False, u'连接数据库出错! => {}'.format(e)
        return conn

    def diff_data(self, left=[], right=[], exclude=[], result_folder='.'):
        """
        数据对比
        | :param left: 从接口获取的实际数据结果, 必须是字典list或者数据源文件路径
        | :param right: 从数据库查询的预期数据结果, 必须是字典list或者数据源文件路径
        | :param exclude: 不需要对比的字段
        | :param result_folder: 结果保存目录路径
        | :return: 无
        """
        if result_folder == '.' or not os.path.isdir(result_folder):
            result_folder = os.path.normpath(os.path.abspath(self.result_folder))
        else:
            result_folder = os.path.normpath(os.path.abspath(result_folder))
        result_folder = os.path.normpath('{}/{}'.format(result_folder, time.strftime('%Y%m%d')))
        if not os.path.isdir(result_folder):
            os.makedirs(result_folder)
        now = '{}.{}'.format(time.strftime('%H%M%S'), repr(time.time()).split('.')[1])
        source_left_file = os.path.normpath('{}/source_{}_left.txt'.format(result_folder, now))
        source_right_file = os.path.normpath('{}/source_{}_right.txt'.format(result_folder, now))
        diff_result_file = os.path.normpath('{}/diff_{}_result.diff'.format(result_folder, now))
        diff_result_html = os.path.normpath('{}/diff_{}_result.html'.format(result_folder, now))
        if isinstance(left, str) and os.path.isfile(left):
            source_left_file = left
            with open(left, 'r', encoding='utf8') as fp:
                l = fp.readlines()
            msg = u'[实际结果] 原始数据保存在 {} 中, 共 {} 条\n'.format(left, len(l))
            left = []
            for row in l:
                left.append(json.loads(row))
        else:
            if not isinstance(left, list):
                left = ast.literal_eval(left)
            with open(source_left_file, 'w', encoding='utf8') as fp:
                num = 0
                for row in left:
                    row = json.dumps(self.__parse_none_to_empty_as_dict(row), sort_keys=True, ensure_ascii=False)
                    fp.writelines('{}\n'.format(row))
                    num += 1
            msg = u'[实际结果] 原始数据保存在 {} 中, 共 {} 条\n'.format(source_left_file, num)
        if isinstance(right, str) and os.path.isfile(right):
            source_right_file = right
            with open(right, 'r', encoding='utf8') as fp:
                r = fp.readlines()
            msg = u'{}[预期结果] 原始数据保存在 {} 中, 共 {} 条\n'.format(msg, right, len(r))
            right = []
            for row in r:
                right.append(json.loads(row))
        else:
            if not isinstance(right, list):
                right = ast.literal_eval(right)
            with open(source_right_file, 'w', encoding='utf8') as fp:
                num = 0
                for row in right:
                    row = json.dumps(self.__parse_none_to_empty_as_dict(row), sort_keys=True, ensure_ascii=False)
                    fp.writelines('{}\n'.format(row))
                    num += 1
            msg = u'{}[预期结果] 原始数据保存在 {} 中, 共 {} 条\n'.format(msg, source_right_file, num)
        if not isinstance(exclude, list):
            exclude = ast.literal_eval(exclude)
        # if len(left) > 0 and isinstance(left, list) and len(right) > 0 and isinstance(right, list):
        #     if not isinstance(left[0], dict) or not isinstance(right[0], dict):
        #         assert False, u'对比的两个数据源必须是字典列表! Left: {}  Right: {}'.format(type(left[0]), type(right[0]))
        # else:
        #     assert False, u'对比的两个数据源必须是列表并且不能为空! Left: {} #{}  Right: {} #{}'.format(type(left), len(left), type(right), len(right))
        if len(left) > 0 and isinstance(left, list) and isinstance(left[0], dict) and len(right) > 0 and isinstance(right, list) and isinstance(right[0], dict):
            for key in exclude:
                for row in left:
                    key_split = key.split('.')
                    if len(key_split) >= 2:
                        if row[key_split[0]] is not None:
                            if not isinstance(row[key_split[0]], list):
                                row[key_split[0]] = ast.literal_eval(row[key_split[0]])
                            row[key_split[0]] = sorted(row[key_split[0]])
                            for i in range(len(row[key_split[0]])):
                                if not isinstance(key_split[1], list):
                                    key_split[1] = ast.literal_eval(key_split[1])
                                for line in key_split[1]:
                                    row[key_split[0]][i][line] = ''
                                    row[key_split[0]][i] = json.loads(json.dumps(row[key_split[0]][i], sort_keys=True))
                    else:
                        row[key_split[0]] = ''
                for row in right:
                    key_split = key.split('.')
                    if len(key_split) >= 2:
                        if row[key_split[0]] is not None:
                            if not isinstance(row[key_split[0]], list):
                                row[key_split[0]] = ast.literal_eval(row[key_split[0]])
                            row[key_split[0]] = sorted(row[key_split[0]])
                            for i in range(len(row[key_split[0]])):
                                if not isinstance(key_split[1], list):
                                    key_split[1] = ast.literal_eval(key_split[1])
                                for line in key_split[1]:
                                    row[key_split[0]][i][line] = ''
                                    row[key_split[0]][i] = json.loads(json.dumps(row[key_split[0]][i], sort_keys=True))
                    else:
                        row[key_split[0]] = ''
        result = True
        for i in range(len(left)):
                left[i] = '{}\n'.format(json.dumps(left[i], sort_keys=True, ensure_ascii=False))
        for i in range(len(right)):
            right[i] = '{}\n'.format(json.dumps(right[i], sort_keys=True, ensure_ascii=False))
        left = sorted(left)
        right = sorted(right)
        if left != right:
            result = False
            with open(diff_result_file, 'w', encoding='utf8') as fp:
                diff = difflib.unified_diff(left, right, source_left_file, source_right_file)
                fp.writelines(diff)
            """with open(diff_result_html, 'wb') as fp:
                diff = difflib.HtmlDiff().make_file(left, right, '实际结果({})'.format(source_left_file), 
                                                    '预期结果({})'.format(source_right_file), context=True)
                fp.writelines(diff.replace('charset=ISO-8859-1', 'charset=utf8'))"""
            msg = u'{}[实际结果] 与 [预期结果] 之间存在差异, 对比结果保存在 {} 中\n'.format(msg, diff_result_file)
        print(msg)
        assert result, msg

# if __name__ == '__main__':
#     t = DataDiffLibrary()
#     cookie = t.login_interface('http://be.xiaoniu88.com:8000/be/login', {"username": "admin",
#                         "password": "be5a7e7b9ab70b4a39836465cae867d7c3b8508eb67945a0f5e9a5c5a0878dc449b9e2c729f8847488a6458ec23f42ac68aea225669ab31522e4b730b4937aa713fc7b57e506d61b40551925f3683cc0580e459900f1694b1c81c320e2c0a133547e667d560ddf6e403785f12833a7a8ac0a7c31124c17ce0633c841b7903949",
#                         "captcha": ""})
#     print(cookie)