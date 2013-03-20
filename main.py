__author__ = 'Will Crawford <will@metawhimsy.com>'
from flask import Flask
import config
from session import ItsdangerousSessionInterface
from database import init_engine, db_session

app = Flask(__name__.split('.')[0])
app.config.from_object(config.PycharmDev)
app.session_interface = ItsdangerousSessionInterface()
init_engine(app.config['DATABASE_URI'],
                           convert_unicode=True)
from database import db_session
import views

@app.teardown_request # This decorator calls this function when a request is finished.
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    if app.config['DEBUG']:
        use_debugger = True
        from database import init_db
        init_db()
    if app.config['DEBUG_WITH_PYCHARM']:
        use_debugger = not (app.config.get('DEBUG_WITH_PYCHARM'))
    app.run(use_debugger=use_debugger, port=1234)
    
