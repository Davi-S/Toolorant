import flask

def init_app(app: flask.Flask):
    @app.route('/')
    def warning_page():
        return 'Please open valorant and restart Toolorant'
    
    @app.before_request
    def before_request():
        if flask.request.endpoint != 'warning_page':
            return flask.redirect(flask.url_for('warning_page'))


