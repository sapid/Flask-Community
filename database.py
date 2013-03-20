__author__ = 'Will Crawford <will@metawhimsy.com>'
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, create_session
from sqlalchemy.ext.declarative import declarative_base

engine = None
db_session = scoped_session(lambda: create_session(autocommit=False,
                                                   autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_engine(uri, **kwargs):
   global engine 
   engine = create_engine(uri, convert_unicode=True)
   return engine
   

def init_db():
   # import all modules here that might define models so that
   # they will be registered properly on the metadata.  Otherwise
   # we will have to import them first before calling init_db()
   import models
   Base.metadata.create_all(bind=engine)