#!flask/bin/python3.6
# -*- coding: utf-8 -*-
from flask import Blueprint

USERS = Blueprint('Users', __name__)

from . import users
