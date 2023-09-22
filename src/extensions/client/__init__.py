import flask

from .client import CustomClient


def init_app(app: flask.Flask):
    app.client = CustomClient()
    app.logger.debug('Client extension loaded successfully')