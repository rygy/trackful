import os 


class DevelopmentConfig(object):
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///tracky-development.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://ojqyfpjplpvcwo:8h_grVohK3XZVOsOFyTCAba-Ri@ec2-23-23-80-55.compute-1.amazonaws.com:5432/d1ltr1o4qvn18d'
    DEBUG = True
    SECRET_KEY = os.environ.get('BLOGFUL_SECRET_KEY', 'SECRET')


class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///tracky-testing.db"
    DEBUG = False
    SECRET_KEY = 'NOT SECRET'

