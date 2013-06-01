__author__ = 'Will Crawford <will@metawhimsy.com>'
from main import app

if __name__ == '__main__':
    if app.config['DEBUG']:
        use_debugger = True
        from database import init_db

        init_db()
    if app.config['DEBUG_WITH_PYCHARM']:
        use_debugger = not (app.config.get('DEBUG_WITH_PYCHARM'))
    app.run(use_debugger=use_debugger, port=1234)
    