import logging

import flask
import valclient.exceptions


logger = logging.getLogger(__name__)

index_bp = flask.Blueprint('index',
                           __name__,
                           template_folder='templates')


@index_bp.before_app_request
def check_connection():
    app = flask.current_app
    if not app.config.get('CHECK_CONNECTION', True):
        return

    if flask.request.endpoint in ['static', 'index.no_valorant', None]:
        return

    if not app.websocket.is_running:
        logger.warn('Websocket and/or Client is not running. Trying to start them')
        try:
            client = app.client.activate()
            app.websocket.start(
                client.lockfile['port'],
                client.lockfile['password']
                )
            logger.warn('Websocket and Client started successfully')
            return
        except valclient.exceptions.HandshakeError as e:
            logger.error(f'Could not start the Websocket and/or Client due to error: {e}')
            return flask.redirect(flask.url_for('index.no_valorant'))


@index_bp.after_app_request
def after_request(response: flask.Response):
    request = flask.request
    if request.endpoint:
        flask.current_app.logger.info(
            f'[{request.method:<7}] [{response.status_code:<3}] [{request.path}] - {request.endpoint}'
        )
    return response


@index_bp.route('/')
def index():
    return flask.render_template('index/index.html')


@index_bp.route('/no-valorant')
def no_valorant():
    return flask.render_template('index/no-valorant.html')


@index_bp.route('/in-development')
def in_development():
    return flask.render_template('index/in-development.html')