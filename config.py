from __future__ import absolute_import

import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    def __init__(self):
        pass

    DEBUG = True

    SECRET_KEY = 'This string will be replaced with a proper key in production.'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/ote_deliveries'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    REQUEST_HEADERS = {
        'Accept': 'application/json'
    }

    LOGFILE = '{}/logs/log.log'.format(_basedir)

    AUTH_USERNAME = 'ote'
    AUTH_PASSWORD = 'Keny@21%'
    SECRET = ",\x85\x1f\t\r\xd7'\xda\xd2\xa23\x10\xddW\xe4\x141\xb78Mu\x16\rP%\xe6m\xf4xoi\x93"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self)


class ProductionConfig(DevelopmentConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/ote_deliveries'


config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}