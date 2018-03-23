#!flask/bin/python3
# -*- coding: utf-8 -*-

# 程序运行环境，如果是开发环境，Dev = True，如果是生产环境，Dev = False
# 待完善--这个环境目前还没有被调用
APP_ENVIRONMENT = {

    'DEV': True
}

# MongoDB 服务器设置。
# 待完善--后面要加上判断，开发环境和生产环境自动区分。
MONGODB_CONFIG = {
    'host': '192.168.31.35',
    'port': 27017,
    'db_name': 'testdb',
    'username': 'pmptikutest',
    'password': '123456'
}

# 这个信息框，定义了API在接到访问后返回给用户的各种信息。
# 待完善--后面要加上判断，开发环境和生产环境区分。
MESSAGE_SEND_TO_CLIENT = {

}
