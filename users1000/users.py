#!flask/bin/python3
# -*- coding: utf-8 -*-
from flask_restful import Resource, Api, reqparse
from . import USERS
from db1000.myconn import find, insert, find_one, select_colum

ApiBlue = Api(USERS)


#
# def findeuser(valus):
#     users = find_one("users", valus)
#
#     return users


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
    # def del(self):


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
            return {'code': '200', 'messages': 'registered successfully'
                    }
        except Exception as e:
            return str(e)


class UserTest(Resource):

    def get(self):
        readme = "this is Test motheds."
        return readme

    def post(self):
        args = parser.parse_args()
        usersname = {'usersname': args['username']}
        users = find_one("users", usersname)

        return users


ApiBlue.add_resource(UserList, '/')
ApiBlue.add_resource(UserSingUp, '/singup')
ApiBlue.add_resource(UserTest, '/test')
