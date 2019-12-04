#!./env/bin/python
from __future__ import absolute_import

import logging
import os
from logging.handlers import RotatingFileHandler

from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Shell, Manager, prompt_bool

from app import create_app, db

application = create_app(os.getenv('FLASK_CONFIG') or 'default')

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


def _context():
    return {'app': application, 'db': db}


db_manager = Manager(usage='database commands')
migrate = Migrate(application, db)


@db_manager.command
def drop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@db_manager.command
def create():
    db.create_all()


manager = Manager(application)
manager.add_command("runserver", Server(port=9000))
manager.add_command("shell", Shell(make_context=_context))
manager.add_command("database", db_manager)
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    applogger = application.logger

    file_handler = RotatingFileHandler('./error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    application.logger.addHandler(file_handler)
    application.logger.setLevel(logging.DEBUG)

    manager.run()