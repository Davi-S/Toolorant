import flask

watcher_bp = flask.Blueprint('watcher_bp', __name__,
                             template_folder='templates')


def init_app(app: flask.Flask):
    app.register_blueprint(watcher_bp)
    app.before_request(before_request_function)


def before_request_function():
    # Cancel the original request and render the error template if the websocket is not running
    if not flask.current_app.websocket.is_running:
        # Not blocking static endpoints (CSS and JS)
        if flask.request.endpoint == 'static':
            return
        return flask.render_template('valorant_watcher/error_message.html')
    return
