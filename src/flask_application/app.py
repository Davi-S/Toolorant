# TODO: Give name to all new threads created on the application
# TODO: Add logging to all files
import contextlib

import flask

from .configuration import with_dynaconf


def create_app(environment: str = 'development') -> flask.Flask:
    app = flask.Flask(__name__)
    # Init the extensions and configurations with dynaconf
    with_dynaconf.init_app(app, environment)

    # Suppressing errors while loading the client/ws when trying to open the application with valorant closed
    # TODO: suppress the right and specific error
    with contextlib.suppress(Exception):
        app.client.activate()
        app.websocket.start(app.client.lockfile)

    return app
