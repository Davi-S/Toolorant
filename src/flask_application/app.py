import flask
from .configuration import with_dynaconf
from .client.client import CustomClient

# TODO: uncomment this
def create_app(environment: str = 'development') -> flask.Flask:
    app = flask.Flask(__name__)
    
    # Try to activate the client (check if valorant is open).
    # If the valorant is not open, the application is unusable.
    # If the valorant is open, proceed with the initialization.
    # try: 
    #     CustomClient().activate()
    # except Exception:
    #     @app.route('/')
    #     def warning_page():
    #         return 'Please open valorant and restart the instalocker to use the application'
    #     @app.before_request
    #     def before_request():
    #         if flask.request.endpoint != 'warning_page':
    #             return flask.redirect(flask.url_for('warning_page'))
    #     return app
    
    # Init the application
    with_dynaconf.init_app(app, environment)
    # app.client.activate()
    # app.websocket.start(app.client.lockfile)
    return app

