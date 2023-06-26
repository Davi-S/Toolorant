import flask

from .client.client import CustomClient
from .configuration import with_dynaconf
from .no_valorant import no_valorant


# TODO: uncomment this
def create_app(environment: str = 'development') -> flask.Flask:
    app = flask.Flask(__name__)
    # Check if valorant is open.
    # If the valorant is not open, the application is unusable.
    # If the valorant is open, proceed with the initialization.
    # TODO: Need to add a way to load this if the valorant is closed while the application is running
    try: 
        CustomClient().activate()
    except Exception:
        no_valorant.init_app(app)
        return app
    
    # Init the application
    with_dynaconf.init_app(app, environment)
    app.client.activate()
    app.websocket.start(app.client.lockfile)
    return app

