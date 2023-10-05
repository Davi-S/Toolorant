# python src\blueprints\stream_hunter\stream_hunter.py
import logging

import flask


logger = logging.getLogger(__name__)

stream_hunter_bp = flask.Blueprint('stream_hunter',
                                   __name__,
                                   template_folder='templates')


@stream_hunter_bp.route('/')
def index():
    return flask.render_template(
        'stream_hunter/stream_hunter.html'
    )


@stream_hunter_bp.route('/streams')
def streams():
    streams_data = stream_hunter_bp.stream_hunter.hunt()
    return flask.jsonify(streams_data)
