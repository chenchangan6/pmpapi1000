#!flask/bin/python3
# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from . import USERS
from db1000.myconn import find, insert

ApiBlue = Api(USERS)


# 用来获取用户列表。
class UserList(Resource):

    def get(self):

        try:
            user_list = []
            userlist = find("users", {})
            for x in userlist:
                x.pop("_id")
                user_list.append(x)
            return user_list
        except Exception as e:
            return str(e)


# 待完善--后面要将用户名和密码参数改为 required = True.
parser = reqparse.RequestParser()
parser.add_argument('username', required=True, location='json')
parser.add_argument('pwd', required=True, location='json')
parser.add_argument('nickname', required=True, location='json')


class UserSingUp(Resource):

    def get(self):
        mothoed_reademe = "this is users sing-up mothed."

        return mothoed_reademe

    def post(self):
        args = parser.parse_args()
        try:
            insert("users", args)
            return '200'
        except Exception as e:
            return str(e)


ApiBlue.add_resource(UserList, '/')
ApiBlue.add_resource(UserSingUp, '/singup')
