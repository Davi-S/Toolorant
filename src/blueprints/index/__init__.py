import flask

from .index import index_bp


def init_app(app: flask.Flask):
    app.register_blueprint(index_bp)
    app.logger.debug('Index blueprint registered successfully')