import logging

from logging_configuration import create_file_handler

from .client import CustomClient

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

def init_app(app):
    app.client = CustomClient()
    log.info('Client extension loaded on app')