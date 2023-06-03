import flask
from ...instalocker import client
import threading

index_bp = flask.Blueprint('index_bp', __name__,
                           template_folder='templates')


def init_app(app: flask.Flask):
    app.register_blueprint(index_bp)


@index_bp.route('/')
def index():
    return flask.render_template('index/index.html')

