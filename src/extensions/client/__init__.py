import flask

from .client import CustomClient


def init_app(app: flask.Flask):
    # Giving default region to not get a RegionError when starting with valorant closed
    app.client = CustomClient('na')
    app.logger.debug('Client extension loaded successfully')