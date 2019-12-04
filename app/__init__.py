from __future__ import absolute_import

import datetime
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_name):
    application = Flask(__name__)
    application.config.from_object(config[config_name])

    from .customer import customer

    db.init_app(application)
    bcrypt.init_app(application)
    CORS(application)

    application.register_blueprint(customer)

    file_handler = RotatingFileHandler(application.config['LOGFILE'], maxBytes=20971520, backupCount=5, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = '%(asctime)s [%(filename)s:%(lineno)d] : %(message)s'
    file_formatter = logging.Formatter(file_format)
    file_handler.setFormatter(file_formatter)
    application.logger.addHandler(file_handler)

    @application.before_first_request
    def initialize_queue():
        pass

    @application.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE')
        return response

    @application.route('/')
    def ote_welcome():
        return 'Ote Deliveries v1.0', 200

    return application


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now)
    last_modified = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now, onupdate=datetime.datetime.now)