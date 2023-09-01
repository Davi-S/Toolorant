import logging

import flask

from logging_configuration import create_file_handler


# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

index_bp = flask.Blueprint('index_bp', __name__,
                           template_folder='templates')


def init_app(app: flask.Flask):
    app.register_blueprint(index_bp)
    log.info('Index blueprint registered')


@index_bp.route('/')
def index():
    return flask.render_template('index/index.html')


@index_bp.route('/in-development')
def in_development():
    return flask.render_template('index/in_development.html')
