#!/usr/bin/env python
import os

from flask_jwt import JWT

from app.api_1_0.models import InnerResult
from app.datasource.models import OriginData

COV = None

if os.environ.get("FLASK_COVERAGE"):
    import coverage
    # TODO:here is not understand
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

if os.path.exists('.env'):
    '''import env config'''
    print('Importing environment from .env ...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
from flask_script import Manager, Shell
from app.models import User, Role, Permission
from flask_migrate import MigrateCommand, Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return user


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter_by(id=user_id).first()
    return user

jwt = JWT(app, authenticate, identity)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission,
                InnerResult=InnerResult, OriginData=OriginData)

migrate = Migrate(app, db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()
