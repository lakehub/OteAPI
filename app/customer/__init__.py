from __future__ import absolute_import

from flask import Blueprint
from flask_restful import Api

from . import resource

customer = Blueprint('customer', __name__)

api = Api(customer)

api.add_resource(resource.CustomerResource, '/customer', endpoint='/customer')