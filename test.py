#!flask/bin/python3
# -*- coding: utf-8 -*-
from  flask_restful import Resource, Api



class test(Resource):

    def get(self):

        return "is here"


