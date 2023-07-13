import flask

from .client.client import CustomClient
from .configuration import with_dynaconf


def create_app(environment: str = 'development') -> flask.Flask:
    app = flask.Flask(__name__)
    # TODO: Check if valorant is open using the websocket
    # TODO: Find a way to stop the application if valorant is closed
    # Check if valorant is open.
    # If the valorant is not open, the application is unusable.
    # If the valorant is open, proceed with the initialization.
    # try: 
    #     CustomClient().activate()
    # except Exception:
    #     # Return app without initializing it
    #     return app
    
    # Init the application
    with_dynaconf.init_app(app, environment)
    # app.client.activate()
    # app.websocket.start(app.client.lockfile)
    return app

