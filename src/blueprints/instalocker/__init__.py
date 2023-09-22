import flask

from .instalocker import instalocker_bp
from .instalocker_cls import Instalocker
from .profile import Profile


def init_app(app: flask.Flask):
    instalocker = Instalocker(
        app.client,
        app.user_settings.instalocker.select_delay,
        app.user_settings.instalocker.lock_delay
    )
    profile_name = app.user_settings.instalocker.profile
    instalocker.profile = None if profile_name is None else Profile.load(profile_name)
    instalocker_bp.instalocker = instalocker
    app.register_blueprint(instalocker_bp, url_prefix='/instalocker')
    app.logger.debug('Instalocker blueprint registered successfully')
