__author__ = 'Will Crawford <will@metawhimsy.com>'


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///db.sqlite' # sqlite by default


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'insecure dev key that should be changed'


class PycharmDev(Config):
    DEBUG = True
    SECRET_KEY = 'insecure dev key that should be changed'
    DEBUG_WITH_PYCHARM = True


class TestingConfig(Config):
    TESTING = True