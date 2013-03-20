__author__ = 'Will Crawford <will@metawhimsy.com>'
from flask import Flask
import config
from session import ItsdangerousSessionInterface
from database import init_engine, db_session

def create_app(c):
   app = Flask(__name__)
   app.config.from_object(c)
   app.session_interface = ItsdangerousSessionInterface()
   init_engine(app.config['DATABASE_URI'])
   return app
                                                          
if __name__ == '__main__':
   global app
   app = create_app(config.PycharmDev)
   if app.config['DEBUG']:
      from database import init_db
      init_db()
      use_debugger = True
   if app.config['DEBUG_WITH_PYCHARM']:
      use_debugger = not(app.config.get('DEBUG_WITH_PYCHARM'))
   app.run(use_debugger=use_debugger, port=5000)

@app.teardown_request # This decorator calls this function when a request is finished.
def shutdown_session(exception=None):
   db_session.remove()

@app.route('/')
def hello_world():
   return 'Hello World!'
