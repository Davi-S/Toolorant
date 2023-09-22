import flask

from .websocket import WebSocket


def init_app(app: flask.Flask):
    app.websocket = WebSocket()
    app.logger.debug('Websocket extension loaded successfully')
