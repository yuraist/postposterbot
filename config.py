import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    use_reloader = False
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'nJA40Kfl9nfds25ufnv12vwn'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = b'awfke'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECURITY_USER_IDENTITY_ATTRIBUTES = ['username']


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
