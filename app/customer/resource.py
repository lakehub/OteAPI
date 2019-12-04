from __future__ import absolute_import

from flask import current_app, request
from flask_restful import Resource, reqparse

import time, datetime

from app import bcrypt
from .. import db
from ..constants import ROLE_CUSTOMER
from ..models import UserModel
from ..utils import verify_basic_auth

__author__ = 'Simeon'


class CustomerResource(Resource):
    def __init__(self):
        super(self.__class__, self).__init__()

    def post(self):
        # authorization
        auth_username = request.authorization["username"] if request.authorization else False
        auth_password = request.authorization["password"] if request.authorization else False

        if not verify_basic_auth(auth_username, auth_password):
            return {
                       'success': False,
                       'message': 'Access denied'
                   }, 401

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', required=True, help='name')
        parser.add_argument('email', required=True, help='email')
        parser.add_argument('phone', required=True, help='phone number')
        parser.add_argument('password', required=True, help='password')

        args = parser.parse_args()
        args['password'] = bcrypt.generate_password_hash(args['password']).decode('UTF-8')
        args['role'] = ROLE_CUSTOMER
        args['public_id'] = str(int(time.mktime(datetime.datetime.utcnow().timetuple())))

        new_user = UserModel(**args)

        try:
            db.session.add(new_user)
            db.session.commit()

            return {
                       'success': True,
                       'message': 'record added successfully!'
                   }, 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e, exc_info=True)
            return {
                       'success': False,
                       'message': 'something went wrong when adding record. Please try again later.'
                   }, 500
