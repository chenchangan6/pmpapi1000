#!flask/bin/python3.6
# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask_restful import Resource, Api
from users1000.users import USERS
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)
INDEX = Blueprint('index', __name__)
ApiBlue = Api(INDEX)


class HelloWorld(Resource):
    def get(self):
        cc = random.randint(0, 100)
        return {'启动成功': 200, '随机数': cc}


ApiBlue.add_resource(HelloWorld, '/')
app.register_blueprint(INDEX, url_prefix='/')
app.register_blueprint(USERS, url_prefix='/users')
if __name__ == '__main__':
    app.run(debug=True)
