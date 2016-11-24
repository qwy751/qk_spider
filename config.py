import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\xfbT#4\x87T\xa4\x8cS\xee\xdc\xca}\xd1\x12\x96fe\xaf,ij\xdd\xa8'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'noreply@qkjr.com.cn'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Admin945'
    FLASKY_MAIL_SUBJECT_PREFIX = '[QKJR_SPIDER]'
    FLASKY_MAIL_SENDER = 'spider <noreply@qkjr.com.cn>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    JWT_AUTH_URL_RULE = '/api/v1.0/auth'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'spider-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'spider-test.sqlite')
    WTF_CSRF_ENABLED = False

    SERVER_NAME = '127.0.0.1:5000'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
