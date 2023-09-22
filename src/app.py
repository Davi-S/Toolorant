import flask

import config.flask_config


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)
    # Load settings and extensions from file 
    config.flask_config.init_app(app)
    return app