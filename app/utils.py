from __future__ import absolute_import

from flask import current_app


def verify_basic_auth(username, password):
    if (username == current_app.config['AUTH_USERNAME']) and (password == current_app.config['AUTH_PASSWORD']):
        return True

    return False