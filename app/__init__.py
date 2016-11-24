# -*- coding: utf-8 -*-
from flask import Flask
from flask_oauthlib.provider import OAuth2Provider
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask_restful import Api
import logging
from oauthlib import oauth2

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
oauth = OAuth2Provider()
api = Api()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)

    # TODO:先简单的创建日志文件
    log_handler = logging.FileHandler('flask.log')
    app.logger.addHandler(log_handler)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .main import main as main_blueprint
    #app.register_blueprint(main_blueprint)

    from .enterprise import enterprise as enterprise_blueprint
    app.register_blueprint(enterprise_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .datasource import ds as ds_blueprint
    app.register_blueprint(ds_blueprint, url_prefix='/ds')

    from .api_1_0 import api as api_1_0_blueprint
    api.init_app(api_1_0_blueprint)
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app

