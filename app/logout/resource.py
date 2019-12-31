from __future__ import absolute_import

from flask_restful import Resource, request, reqparse

from ..utils import verify_basic_auth
from ..models import BlacklistTokenModel

__author__ = 'Simeon'


class LogoutResource(Resource):
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
