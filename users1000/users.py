#!flask/bin/python3
# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from . import USERS
from db1000.myconn import find_desc, insert, select_colum, delete_many

ApiBlue = Api(USERS)


# 待完善--为方法名称写上详细的注释。和用例。


# 检查是否存在，用户名或者昵称：例如：tables='users',values= {'username': 'cca'},filed='username'
def findeuser(tables, valus, filed):
    res = select_colum(tables, valus, filed)

    resoult = []
    for k in res:
        resoult.append(k)

    resoult.append({'len': len(resoult)})

    return resoult


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
        mothoed_reademe = "this is users sing-up mothed."
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
                insert("users", args)
                return {'code': '200', 'messages': 'registered successfully'}
            return {'code': '404', 'messages': 'user is registerd'}
        except Exception as e:
            return str(e)


# 临时测试项目
class UserTest(Resource):

    def get(self):
        readme = 'this is Test motheds.'
        return readme


ApiBlue.add_resource(UserList, '/')
ApiBlue.add_resource(UserSingUp, '/singup')
ApiBlue.add_resource(UserDelete, '/delete')
ApiBlue.add_resource(UserTest, '/test')
