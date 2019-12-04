from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api

from . import resource

validate = Blueprint('validate', __name__)

api = Api(validate)

api.add_resource(resource.ValidateResource, '/validate', endpoint='/validate')