import logging

import flask

from logging_configuration import create_file_handler


# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

watcher_bp = flask.Blueprint('watcher_bp', __name__,
                             template_folder='templates')


def init_app(app: flask.Flask):
    app.register_blueprint(watcher_bp)
    app.before_request(before_request_function)
    log.info('Valorant watcher blueprint registered')    


def before_request_function():
    # Cancel the original request and render the error template if the websocket is not running
    if not flask.current_app.websocket.is_running:
        # Not blocking static endpoints (CSS and JS)
        if flask.request.endpoint == 'static':
            return
        log.info(f'Blocked request: {flask.request}')
        return flask.render_template('valorant_watcher/error_message.html')
    return
