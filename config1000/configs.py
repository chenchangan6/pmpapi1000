#!flask/bin/python3.6
# -*- coding: utf-8 -*-
# -*- author: Charles Chen
# 程序运行环境，如果是开发环境，Dev = True，如果是生产环境，Dev = False
# 待完善--这个环境目前还没有被调用
APP_ENVIRONMENT = {

    'DEV': True
}

# MongoDB 服务器设置。
# 待完善--后面要加上判断，开发环境和生产环境自动区分。
MONGODB_CONFIG = {
    'host': '180.76.121.121',
    'port': 27017,
    'db_name': 'testdb',
    'username': 'pmptikutest',
    'password': '123456'
}

# 关于用户密码加密的设置。tokenexpiration单位为秒，设置的TOKEN过期时间
USERPASSWORD_CONFIG = {

    'hashpasswordaddsalt': 'pmptiku.com',
    'tokensecretkey': 'token@pmptiku.com',
    'tokenexpiration': 1 * 24

}
# 用户手机验证码过期时间，单位为分钟。
USERVERIFYCODE_CONFIG = {
    'appid': 1400092769,
    'appkey': '7b66a09ffdf112caf9150642ed555031',
    'template_id': 121466,
    'expirtime': 5

}

# 这个信息框，定义了API在接到访问后返回给用户的各种信息。
# 待完善--后面要加上判断，开发环境和生产环境区分。
MESSAGE_SEND_TO_CLIENT = {

}
