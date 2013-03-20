__author__ = 'Will Crawford <will@metawhimsy.com>'

class Config(object):
   DEBUG = False
   TESTING = False
   DATABASE_URI = 'sqlite:///db.sqlite' # sqlite by default

class ProductionConfig(Config):
   DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
   DEBUG = True

class PycharmDev(Config):
   DEBUG = True
   DEBUG_WITH_PYCHARM = True

class TestingConfig(Config):
   TESTING = True