from .websocket import WebSocket


def init_app(app):
    app.websocket = WebSocket()
