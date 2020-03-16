# coding=utf8
from Resource.common_veriables import *
from Core.Libs import DatabaseLibrary
from faker import Faker
from sshtunnel import SSHTunnelForwarder
from hashlib import md5
import base64
import paramiko
import math
import random
import redis
import json


class CommonLibrary(object):
    def __init__(self):
        self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        self.db = DatabaseLibrary()
        self.fake = Faker(['zh_CN'])

    def mysql_query(self, sql, host=db_host, port=db_port, user=db_user, passwd=db_passwd, db_name=db_name, res_dict=True):
        """执行MYSQL查询语句"""
        with self.mysql_connect() as mysql_ssh:
            db_connect_string="database='{}', user='{}', password='{}', host='{}', port={}, charset='UTF8'".format(
                db_name, user, passwd, mysql_ssh.local_bind_host, mysql_ssh.local_bind_port)
            if res_dict:
                db_connect_string += ', cursorclass=db_api_2.cursors.DictCursor'
            self.db.connect_to_database_using_custom_params(
                dbapiModuleName='pymysql', db_connect_string='{}'.format(db_connect_string)) 
            result = self.db.query(sql)
            self.db.disconnect_from_database()
        return result

    def mysql_update(self, sql, host=db_host, port=db_port, user=db_user, passwd=db_passwd, db_name=db_name):
        """执行MYSQL更新语句"""
        with self.mysql_connect() as mysql_ssh:
            self.db.connect_to_database_using_custom_params(
                dbapiModuleName='pymysql', db_connect_string="database='{}', user='{}', password='{}', host='{}', port={}, charset='UTF8'".format(
                db_name, user, passwd, mysql_ssh.local_bind_host, mysql_ssh.local_bind_port)) 
            self.db.execute_sql_string(sqlString=sql)
            self.db.disconnect_from_database()

    def mysql_connect(self, host=db_host, port=db_port, ssl_keyfile=redis_ssh_key, 
                    ssh_host=redis_ssh_host, ssh_port=redis_ssh_port, ssh_user=redis_ssh_user):
        private_key = paramiko.RSAKey.from_private_key_file(ssl_keyfile)
        return SSHTunnelForwarder((ssh_host, ssh_port), ssh_username=ssh_user, ssh_private_key=private_key, 
                                  remote_bind_address=(host, port))

    def redis_connect(self, host=redis_host, port=redis_port, ssl_keyfile=redis_ssh_key, 
                    ssh_host=redis_ssh_host, ssh_port=redis_ssh_port, ssh_user=redis_ssh_user):
        private_key = paramiko.RSAKey.from_private_key_file(ssl_keyfile)
        return SSHTunnelForwarder((ssh_host, ssh_port), ssh_username=ssh_user, ssh_private_key=private_key, 
                                  remote_bind_address=(host, port))

    def redis_get(self, key, db=0):
        with self.redis_connect() as redis_ssh:
            redis_client = redis.Redis(port=redis_ssh.local_bind_port, db=db, password=redis_passwd, decode_responses=True)
            value = redis_client.get(key)
            redis_client.execute_command('quit')
            return value

    def redis_set(self, key, value, db=0):
        with self.redis_connect() as redis_ssh:
            redis_client = redis.Redis(port=redis_ssh.local_bind_port, db=db, password=redis_passwd, decode_responses=True)
            value = redis_client.set(key, value)
            redis_client.execute_command('quit')
            return value

    def redis_delete(self, key, db=0):
        with self.redis_connect() as redis_ssh:
            redis_client = redis.Redis(port=redis_ssh.local_bind_port, db=db, password=redis_passwd, decode_responses=True)
            value = redis_client.delete(key)
            redis_client.execute_command('quit')
            return value

    def random_mobile(self, ex=0):
        """随机手机号"""
        if isinstance(ex, list):
            ex = random.choice(ex)
        ex = 135 if ex == 0 else ex
        return ex + random.randint(100000000, 99999999)

    def random_username(self, ex='HT'):
        """随机用户名"""
        return ex + random.sample('abcdefghijklmnopqrstufwxyz', 6)

    def random_name(self):
        """随机姓名"""
        return self.fake.name()

    def random_email(self, ext='automation.test'):
        """随机邮箱"""
        return random.sample('abcdefghijklmnopqrstufwxyz', 6) + '@' + ext

    def random_bank_card(self, ex=0):
        """随机卡号"""
        ex = 62258878 if ex == 0 else ex
        return ex + random.randint(10000000, 99999999)
