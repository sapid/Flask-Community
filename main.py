__author__ = 'Will Crawford <will@metawhimsy.com>'
from flask import Flask, g
from flask.ext.login import LoginManager, current_user
import config
from session import ItsdangerousSessionInterface
from database import init_engine, db_session

app = Flask(__name__.split('.')[0])
app.config.from_object(config.PycharmDev) # Toggle production/development
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'mods_login'
app.session_interface = ItsdangerousSessionInterface()
init_engine(app.config['DATABASE_URI'],
            convert_unicode=True)
from database import db_session
import views


@app.before_request
def before_request():
    g.user = current_user

#@app.teardown_request # This decorator calls this function when a request is finished.
#def shutdown_session(exception=None):
#    db_session.remove()
