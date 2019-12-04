from __future__ import absolute_import

from flask_restful import Resource, reqparse
from flask import request, current_app

from ..utils import verify_basic_auth
from ..models import BlacklistTokenModel, UserModel
from ..constants import STATUS_USER_DEACTIVATED, STATUS_USER_PENDING

import jwt

__author__ = 'Simeon'


class ValidateResource(Resource):
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
        parser.add_argument('token', required=True, help='token')

        args = parser.parse_args()

        blacklist_record = BlacklistTokenModel.query.filter_by(token=args['token']).first()

        if blacklist_record:
            return {
                'success': False,
                'message': 'Token is blacklisted. Please login again'
            }, 401

        try:
            data = jwt.decode(args['token'], current_app.config['SECRET'], algorithms=['HS256'])
            user_record = UserModel.query.filter_by(public_id=data['public_id']).first()

            if not user_record:
                return {
                    'success': False,
                    'message': 'token is invalid'
                }, 401

            if user_record.status == STATUS_USER_DEACTIVATED:
                return {
                    'success': False,
                    'message': 'You have been deactivated'
                }, 401

            if user_record.status == STATUS_USER_PENDING:
                return {
                    'success': False,
                    'message': 'Your account is pending'
                }, 401

        except jwt.ExpiredSignatureError:
            return {
                'success': False,
                'message': 'token has expired'
            }, 401

        except jwt.InvalidTokenError:
            return {
                'success': False,
                'message': 'token is invalid'
            }, 401

        return {
            'success': False,
            'message': 'token is valid'
        }, 200
