from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api

from . import resource

login = Blueprint('login', __name__)

api = Api(login)

api.add_resource(resource.LoginResource, '/login', endpoint='/login')