import flask

from .stream_hunter import stream_hunter_bp
from .stream_hunter_cls import StreamHunter


def init_app(app: flask.Flask):
    sh = StreamHunter(
        app.client
    )
    stream_hunter_bp.stream_hunter = sh
    app.register_blueprint(stream_hunter_bp, url_prefix='/stream-hunter')
    app.logger.debug('Stream Hunter blueprint registered successfully')