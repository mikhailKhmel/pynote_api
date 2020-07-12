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

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost:5432/pynote_db'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
