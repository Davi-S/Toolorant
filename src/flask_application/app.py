import flask
from .configuration import with_dynaconf


def create_app(environment: str = 'development') -> flask.Flask:
    app = flask.Flask(__name__)
    with_dynaconf.init_app(app, environment)
    return app
