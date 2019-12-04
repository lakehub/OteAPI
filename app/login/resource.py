from __future__ import absolute_import

import datetime
import jwt
from flask import request, current_app
from flask_restful import Resource, reqparse
from sqlalchemy import or_

from app import bcrypt
from ..constants import STATUS_USER_DEACTIVATED, STATUS_USER_PENDING
from ..models import UserModel
from ..utils import verify_basic_auth

__author__ = 'Simeon'


class LoginResource(Resource):
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
        parser.add_argument('username', required=True, help='username')
        parser.add_argument('password', required=True, help='password')

        args = parser.parse_args()

        user_record = UserModel.query.filter(or_(UserModel.phone==args['username'], UserModel.email==args['username'])).first_or_404()

        if not bcrypt.check_password_hash(user_record.password, args['password']):
            return {
                'success': False,
                'message': 'Email, Phone No or password is incorrect'
            }, 401

        if user_record.status == STATUS_USER_DEACTIVATED:
            return {
                       'success': False,
                       'message': 'You have been deactivated'
                   }, 401

        if user_record.status == STATUS_USER_PENDING:
            return {
                       'success': False,
                       'message': 'Your registration is pending'
                   }, 401

        token = jwt.encode({
                "public_id": user_record.public_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
            }, current_app.config['SECRET'], algorithm='HS256'
        )

        return {
            "success": True,
            "token": token.decode('UTF-8'),
            "details": {
                "name": user_record.name,
                "email": user_record.email,
                "phone": user_record.phone,
                "imageUri": user_record.image_uri
            }
        }, 200
