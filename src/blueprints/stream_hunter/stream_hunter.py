# TODO ask user if he has a API key (on settings page or footer)
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
    # Flask does not accept dicts with tuples as keys, so we make each key become a string and them we can split it on the JS
    modified = {
        '-'.join([key[0], key[1]]): value
        for key, value in streams_data.items()
    }
    return flask.jsonify(modified)
