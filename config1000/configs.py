#!flask/bin/python3
# -*- coding: utf-8 -*-
# MongoDB 服务器设置。
# 待完善--后面要加上判断，开发环境和生产环境自动区分。
MONGODB_CONFIG = {
    'host': '192.168.31.108',
    'port': 27017,
    'db_name': 'test',
    'username': 'pmptikutest',
    'password': '123456'
}
