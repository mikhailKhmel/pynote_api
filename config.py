import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

    @property
    def get_secret_key(self):
        SECRET_KEY = 'very-secret'
        return SECRET_KEY

    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
