#!flask/bin/python3.6
# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from . import USERS
from config1000.configs import USERPASSWORD_CONFIG, USERVERIFYCODE_CONFIG
from db1000.myconn import find_desc, insert, select_colum, delete_many, upsert_one
from passlib.apps import custom_app_context
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS, SignatureExpired, BadSignature
from message1000.mobileverifycode import sing_sender
import datetime
import random
import time

ApiBlue = Api(USERS)


# 待完善--为方法名称写上详细的注释。和用例。


# 获取当前服务器日期
def get_now():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now


# 时间差
# 时间a减去时间b，获得二者的时间差,参数为时间字符串，例如：2017-03-30 16:54:01.660
def get_time_diff(timestra, timestrb):
    if timestra <= timestrb:
        return 0
    ta = time.strptime(timestra, "%Y-%m-%d %H:%M:%S")
    tb = time.strptime(timestrb, "%Y-%m-%d %H:%M:%S")
    y, m, d, H, M, S = ta[0:6]
    datatimea = datetime.datetime(y, m, d, H, M, S)
    y, m, d, H, M, S = tb[0:6]
    datatimeb = datetime.datetime(y, m, d, H, M, S)
    secondsdiff = (datatimea - datatimeb).seconds
    # 两者相加得转换成分钟的时间差
    minutesdiff = round(secondsdiff / 60, 1)
    return minutesdiff


# 添加token和登录历史
def insert_token(username, token, createdate=get_now()):
    try:
        # 检查是否已经存在用户登录信息，如果存在就更新token,不存在就添加。
        upsert_one('loginedtoken', {'username': username}, {'username': username, 'token': token,
                                                            'createdate': createdate})

        try:
            # 添加到用户登录历史，以后分析使用。
            insert('loginhistory', {'username': username, 'createdate': createdate})

            return True
        except Exception as e:
            return str(e)
    except Exception as e:
        return str(e)


# 基本认证
auth = HTTPBasicAuth()
authtoken = HTTPTokenAuth()
authmulti = MultiAuth(auth, authtoken)


@auth.verify_password
def verify_pw(username, pwd):
    haveauser = findeuser("users", {'username': username}, 'username', 'pwd')
    if haveauser[-1]['len'] != 0:
        if verify_password(pwd, haveauser[0]['pwd']):
            return True
    return None


@authtoken.verify_token
def verify_token(token):
    if userverify_token(token):
        logined = findeuser('loginedtoken', {'token': token}, 'username')
        if logined[-1]['len'] == 0:
            return False
        # 用来记录用户的验证历史，开启后每次验证后都会记录到数据库
        # try:
        #     insert_token(logined[0]['username'], token)
        # except Exception as e:
        #     return str(e)
    return True


# 检查是否存在，用户名或者昵称：例如：tables='users',values= {'username': 'cca'},filed='username'
# *filed字段可以接受2个参数，如要显示username和pwd 两个字段，就在调用的时候 'username','pwd'
def findeuser(tables, valus, *filed):
    res = select_colum(tables, valus, filed)

    resoult = []
    for k in res:
        resoult.append(k)

    resoult.append({'len': len(resoult)})

    return resoult


# 用户密码加密。
def hashpassword(value):
    value += USERPASSWORD_CONFIG['hashpasswordaddsalt']  # 加盐
    hashpassworldvalue = custom_app_context.encrypt(value)
    return hashpassworldvalue


# 验证密码 说明：userpassword 输入为用户提交的明文密码。dbpassword为从数据库获取到的加密后的密码。
def verify_password(userpassword, dbpassword):
    userpassword += USERPASSWORD_CONFIG['hashpasswordaddsalt']  # 原密码加密的过程已经进行加盐，所以对比的时候要先加盐。
    return custom_app_context.verify(userpassword, dbpassword)


# 生成token,注value 应为JSON格式。本例会将value进行加密。
def generate_token(value):
    token = TJWSS(USERPASSWORD_CONFIG['tokensecretkey'], expires_in=USERPASSWORD_CONFIG['tokenexpiration'])
    return token.dumps(value)


# 验证token,如果正确则返回解密后的token信息，如果超时，则提示，超时。如果被篡改就提示无效的token。
def userverify_token(value):
    token = TJWSS(USERPASSWORD_CONFIG['tokensecretkey'])
    try:
        data = token.loads(value)
    except SignatureExpired:
        return 'valid token, but expired'
    except BadSignature:
        return 'invalid token'
    # return data #此时返回的data已经解密了。可以看到里面的内容
    return True


# 获取用户列表。
class UserList(Resource):

    def get(self):
        # 倒序获取用户列表
        try:
            user_list = []
            userlist = find_desc("users", "_id")
            for x in userlist:
                user_list.append(x)
            return user_list
        except Exception as e:
            return str(e)


# 删除用户
class UserDelete(Resource):

    def get(self):
        return 'this is a delete users method'

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', required=True, location='json')
            args = parser.parse_args()
            haveauser = findeuser("users", {'username': args['username']}, 'username')
            if haveauser[-1]['len'] != 0:
                delete_many('users', {"username": args['username']})

                return {'code': '200', 'messages': 'users is deleted'}

            return {'code': '404', 'messages': 'The user dos not exist'
                    }
        except Exception as e:
            return str(e)


# 用户注册
class UserSingUp(Resource):
    def get(self):
        mothoed_reademe = 'this is users sing-up method.'
        return mothoed_reademe

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location='json')
        parser.add_argument('pwd', required=True, location='json')
        parser.add_argument('nickname', required=True, location='json')
        parser.add_argument('createdate', default=get_now(), location='json')
        args = parser.parse_args()
        if args['username'] == "" or args['pwd'] == "":
            return {'code': '000', 'messages': 'username or pwd is null'}  # 用户名或密码为空
        try:
            if len(str(int(args['username']))) != 11:
                return {'code': '400', 'messages': 'The username must be a mobile number.'}  # 手机号码验证
        except Exception as e:
            return {'code': '400', 'messages': 'The username must be a mobile number.', 'error': e}

        pwdlength = len(args['pwd'])
        if pwdlength < 6 or pwdlength > 20:
            return {'code': '400', 'messages': 'The pwd length must be between 6 and 20.'}  # 密码长度验证

        try:

            haveauser = findeuser("users", {'username': args['username']}, 'username')
            if haveauser[-1]['len'] == 0:
                args['pwd'] = hashpassword(args['pwd'])  # 对用户密码进行加密处理。
                insert("users", args)
                return {'code': '200', 'messages': 'registered successfully'}
            return {'code': '404', 'messages': 'user is registerd'}
        except Exception as e:
            return str(e)


# 用户登录

class UserlogIn(Resource):
    def get(self):
        mothoed_readme = 'this is users sing-in methods.'
        return mothoed_readme

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location='json')
        parser.add_argument('pwd', required=True, location='json')
        args = parser.parse_args()
        if args['username'] == "" or args['pwd'] == "":
            return {'code': '000', 'messages': 'username or pwd is null'}  # 用户名或密码为空
        haveauser = findeuser("users", {'username': args['username']}, 'username', 'pwd')
        if haveauser[-1]['len'] != 0:
            if verify_password(args['pwd'], haveauser[0]['pwd']):
                token = generate_token({'username': args['username'], 'pwd': args['pwd']})
                inserttoken = insert_token(args['username'], token.decode('ascii'))
                if inserttoken:
                    return {'code': '200', 'messages': 'login successfully', 'token': token.decode('ascii')}  # 登录成功
                else:
                    return {'code': '500', 'error': inserttoken}
            return {'code': '400', 'messages': 'login failure'}  # 密码错误

        return {'code': '404', 'messages': 'The user dos not exist'}  # 用户名错误,用户不存在


# 用户手机验证码
class UserPhoneVerificationcode(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phonenumber')
        parser.add_argument('phoneverifycode', type=int)
        args = parser.parse_args()
        try:
            if len(str(int(args['phonenumber']))) != 11:
                return {'code': '400', 'messages': 'Must be a mobile number.'}  # 手机号码验证
            if len(str(int(args['phoneverifycode']))) != 6:
                return {'code': '400', 'messages': 'Must be 6 numbers.'}  # 验证码是6位数字
        except Exception as e:
            return {'code': '400', 'messages': 'error.', 'error': e}
        try:
            haveauser = findeuser('verifycode',
                                  {'phonenumber': args['phonenumber'], 'verifycode': args['phoneverifycode']},
                                  'createdate')
            # 没有该用户的验证码
            if haveauser[-1]['len'] == 0:
                return {'code': '400', 'message': 'verifycode error'}
            # 验证码过期
            if get_time_diff(get_now(), haveauser[0]['createdate']) > USERVERIFYCODE_CONFIG['expirtime']:
                return {'code': '401', 'message': 'verifycode expire'}
            return {'code': '200', 'message': 'verifycode right'}
        except Exception as e:
            return {'code': '400', 'messages': 'error.', 'error': e}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phonenumber')
        args = parser.parse_args()
        try:
            if len(str(int(args['phonenumber']))) != 11:
                return {'code': '400', 'messages': 'Must be a mobile number.'}  # 手机号码验证
        except Exception as e:
            return {'code': '400', 'messages': 'Must be a mobile number.', 'error': e}
        try:
            verifycode = random.randint(100000, 900000)
            upsert_one('verifycode', {'phonenumber': args['phonenumber']},
                       {'phonenumber': args['phonenumber'], 'verifycode': verifycode, 'createdate': get_now()})
            result = sing_sender(args['phonenumber'], verifycode)
            return {'code': '200', 'messages': 'The verifycode sended to ' + args['phonenumber']}
        except Exception as e:
            return {'code': '500', 'messages': 'have a error', 'error': e}


# 临时测试项目
class UserTest(Resource):
    # 装饰器，登录验证
    # decorators = [authmulti.login_required]

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phonenumber')
        args = parser.parse_args()
        try:
            user_list = []
            userlist = find_desc("verifycode", "_id")
            for x in userlist:
                user_list.append(x)
            return user_list
        except Exception as e:
            return str(e)


def post(self):
    # 验证token
    parser = reqparse.RequestParser()
    parser.add_argument('token')
    args = parser.parse_args()
    verifytoken = userverify_token(args['token'])
    return verifytoken


ApiBlue.add_resource(UserPhoneVerificationcode, '/verifycode')
ApiBlue.add_resource(UserList, '/')
ApiBlue.add_resource(UserSingUp, '/singup')
ApiBlue.add_resource(UserlogIn, '/login')
ApiBlue.add_resource(UserDelete, '/delete')
ApiBlue.add_resource(UserTest, '/test')
