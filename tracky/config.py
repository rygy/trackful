import os 


class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tracky-development.db'
    DEBUG = True
    SECRET_KEY = os.environ.get('BLOGFUL_SECRET_KEY', 'SECRET')


class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///tracky-testing.db"
    DEBUG = False
    SECRET_KEY = 'NOT SECRET'

