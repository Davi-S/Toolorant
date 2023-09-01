import logging 

import flask

from logging_configuration import create_file_handler

from .configuration import with_dynaconf

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

def create_app(environment: str = 'development') -> flask.Flask:
    app = flask.Flask(__name__)
    # Init the extensions and configurations with dynaconf
    with_dynaconf.init_app(app, environment)
    log.debug('Extensions loaded')
    # Suppressing errors while loading the client/ws when trying to open the application with valorant closed
    try:
        app.client.activate()
        app.websocket.start(app.client.lockfile)
    except Exception as e:
        log.warning(f'Not able to start Client or Websocket due to error: """{e}"""')
    
    log.info('Flask app created')
    return app
