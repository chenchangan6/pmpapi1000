#!flask/bin/python3.6
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)


def create_app():
    from users1000.users import USERS as USERS
    app.register_blueprint(USERS, url_prefix="/users")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
