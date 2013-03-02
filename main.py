from flask import Flask
from database import db_session
from session import ItsdangerousSessionInterface
import config
__author__ = 'Will Crawford <will@metawhimsy.com>'

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.session_interface = ItsdangerousSessionInterface()

@app.teardown_request
def shutdown_session(exception=None):
   db_session.remove()

@app.route('/')
def hello_world():
   return 'Hello World!'


if __name__ == '__main__':
   app.run(port=5000)
