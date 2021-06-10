import os

basedir = os.path.abspath(os.path.dirname(__file__))


# heroku sqlalchemy issue
# replace postgres:// with postgresql://
# https://bit.ly/3pDwYrv
def get_database_url(s: str):
    uri = os.getenv(s, "")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    return uri


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = get_database_url('DATABASE_URL')


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
    SQLALCHEMY_DATABASE_URI = get_database_url('DATABASE_URL_TEST')
