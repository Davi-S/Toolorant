import flask

index_bp = flask.Blueprint('index_bp', __name__,
                           template_folder='templates')


def init_app(app: flask.Flask):
    app.register_blueprint(index_bp)


@index_bp.route('/')
def index():
    return flask.render_template('index/index.html')


@index_bp.route('/start', methods=['POST'])
def start_instalocker():
    pass


@index_bp.route('/stop', methods=['POST'])
def stop_instalocker():
    pass
