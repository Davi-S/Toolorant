import logging

from logging_configuration import create_file_handler

from .websocket import WebSocket

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

def init_app(app):
    app.websocket = WebSocket()
    log.info('Websocket extension loaded on app')
