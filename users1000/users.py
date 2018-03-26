#!flask/bin/python3
# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from . import USERS
from db1000.myconn import find_desc, insert, select_colum, delete_many
from passlib.apps import custom_app_context

ApiBlue = Api(USERS)


# 待完善--为方法名称写上详细的注释。和用例。


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
def hashpassword(valule):
    valule += 'pmptiku.com'  # 加盐 pmptiku.com
    hashpassworldvalue = custom_app_context.encrypt(valule)
    return hashpassworldvalue


# 验证密码 说明：userpassword 输入为用户提交的明文密码。dbpassword为从数据库获取到的加密后的密码。
def verify_password(userpassword, dbpassword):
    userpassword += 'pmptiku.com'  # 原密码加密的过程已经进行加盐，所以对比的时候要先加盐。
    return custom_app_context.verify(userpassword, dbpassword)


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
        mothoed_reademe = 'this is users sing-up mothed.'
        return mothoed_reademe

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location='json')
        parser.add_argument('pwd', required=True, location='json')
        parser.add_argument('nickname', required=True, location='json')
        args = parser.parse_args()
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
        mothoed_readme = 'this is users sing-in mothoed.'
        return mothoed_readme

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location='json')
        parser.add_argument('pwd', required=True, location='json')
        args = parser.parse_args()
        haveauser = findeuser("users", {'username': args['username']}, 'username', 'pwd')
        if haveauser[-1]['len'] != 0:
            if verify_password(args['pwd'], haveauser[0]['pwd']):
                return {'code': '200', 'messages': 'login successfully'}  # 登录成功
            return {'code': '400', 'messages': 'login failure'}  # 密码错误
        return {'code': '404', 'messages': 'The user dos not exist'}  # 用户名错误,用户不存在


# 临时测试项目
class UserTest(Resource):

    def get(self):
        readme = 'this is Test motheds.'
        return readme


ApiBlue.add_resource(UserList, '/')
ApiBlue.add_resource(UserSingUp, '/singup')
ApiBlue.add_resource(UserlogIn, '/login')
ApiBlue.add_resource(UserDelete, '/delete')
ApiBlue.add_resource(UserTest, '/test')
