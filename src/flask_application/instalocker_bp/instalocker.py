# TODO: The fact that the profile can be None is bad because it adds a lot of checking. Need to find a way to reduce the amount of checks for this
# TODO: Add feature to set a delay on selecting and locking the character to prevent account suspension
import logging

import flask

from logging_configuration import create_file_handler

from .. import forms
from .. import game_resources as gr
from .instalocker_cls import Instalocker
from .profile import Profile, get_all_profiles


# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

instalocker_bp = flask.Blueprint('instalocker_bp', __name__,
                                 template_folder='templates')


def init_app(app: flask.Flask):
    # Create and configure instalocker
    instalocker = Instalocker(app.client,
                              app.user_settings.instalocker.select_delay,
                              app.user_settings.instalocker.lock_delay)
    profile_name = app.user_settings.instalocker.profile
    instalocker.profile = None if profile_name is None else Profile.load(profile_name)

    instalocker_bp.instalocker = instalocker
    app.register_blueprint(instalocker_bp, url_prefix='/instalocker')
    log.info('Instalocker blueprint registered')


@instalocker_bp.route('/', methods=['GET', 'POST'])
def index():
    log.debug('"index" endpoint called')
    return flask.render_template('instalocker/index.html',
                                 profiles=get_all_profiles(),
                                 selected_profile=instalocker_bp.instalocker.profile,
                                 instalocker_active=flask.session.get('instalocker_active', False),
                                 new_profile_form=forms.NewProfileInfo(),
                                 select_delay=flask.current_app.user_settings.instalocker.select_delay,
                                 lock_delay=flask.current_app.user_settings.instalocker.lock_delay)


@instalocker_bp.route('/set', methods=['POST'])
def set_profile():
    log.debug('"set_profile" endpoint called')
    profile_name = flask.request.form.get('profile_name')
    # Set the profile on the instalocker and on the user settings
    instalocker_bp.instalocker.profile = Profile.load(profile_name)
    flask.current_app.user_settings.instalocker.profile = profile_name
    flask.current_app.user_settings.persist()
    # TODO: add check to see if the profile was set successfully and return a descriptive value. Also add logging
    log.info(f'Profile {profile_name} set')
    return ''


@instalocker_bp.route('/delete', methods=['POST'])
def delete_profile():
    log.debug('"delete_profile" endpoint called')
    profile_name = flask.request.form.get('profile_name')
    # Create a profile object for comparison
    profile = Profile.load(profile_name)
    # Delete the profile file
    Profile.delete(profile_name)
    # Check if the profile deleted was set on the instalocker and/or user settings and remove its references
    if instalocker_bp.instalocker.profile == profile:
        instalocker_bp.instalocker.profile = None
    if flask.current_app.user_settings.instalocker.profile == profile.name:
        flask.current_app.user_settings.instalocker.profile = None
        flask.current_app.user_settings.persist()
    # TODO: add check to see if the profile was deleted successfully and return a descriptive value. Also add logging
    log.info(f'Profile {profile_name} deleted')
    return ''


@instalocker_bp.route('/create', methods=['POST'])
def create_profile():
    log.debug('"create_profile" endpoint called')
    form = forms.NewProfileInfo()
    profile_info = {'name': form.name.data,
                    # Replacing space for underline because of Spike Rush
                    'game_mode': gr.GameMode[form.game_mode.data.upper().replace(' ', '_')],
                    # Dictionary comprehension to dynamically build the map-agent based on the game resources classes and field names.
                    'map_agent': {gr.Map[field_name.upper()]: gr.Agent[field.data.upper()] if field.data.upper() != 'NONE' else None
                                  for field_name, field in form._fields.items()
                                  if field_name.upper() in [game_map.name for game_map in gr.Map]}}
    Profile(profile_info['name'],
            profile_info['game_mode'],
            profile_info['map_agent']).dump()
    # TODO: add check to see if the profile was created successfully and return a descriptive value. Also add logging
    log.info(f'Profile {profile_info["name"]} created')
    return ''


@instalocker_bp.route('/set-select-delay', methods=['POST'])
def set_select_delay():
    log.debug('"set_select_delay" endpoint called')
    select_delay = int(flask.request.form.get('delay'))
    if instalocker_bp.instalocker.select_delay != select_delay:
        instalocker_bp.instalocker.select_delay = select_delay
    if flask.current_app.user_settings.instalocker.select_delay != select_delay:
        flask.current_app.user_settings.instalocker.select_delay = select_delay
        flask.current_app.user_settings.persist()
    log.info(f'Agent select delay of {select_delay} is set')
    return ''


@instalocker_bp.route('/set-lock-delay', methods=['POST'])
def set_lock_delay():
    log.debug('"set_lock_delay" endpoint called')
    lock_delay = int(flask.request.form.get('delay'))
    if instalocker_bp.instalocker.lock_delay != lock_delay:
        instalocker_bp.instalocker.lock_delay = lock_delay
    if flask.current_app.user_settings.instalocker.lock_delay != lock_delay:
        flask.current_app.user_settings.instalocker.lock_delay = lock_delay
        flask.current_app.user_settings.persist()
    log.info(f'Agent lock delay of {lock_delay} is set')
    return ''


@instalocker_bp.route('/start', methods=['POST'])
def start():
    log.debug('"start" endpoint called')
    flask.current_app.websocket.add_listener(instalocker_bp.instalocker)
    flask.session['instalocker_active'] = True
    # TODO: add check to see if the instalocker was started successfully and return a descriptive value. Also add logging
    log.info('Instalocker started')
    return ''


@instalocker_bp.route('/stop', methods=['POST'])
def stop():
    log.debug('"stop" endpoint called')
    flask.current_app.websocket.remove_listener(instalocker_bp.instalocker)
    flask.session["instalocker_active"] = False
    # TODO: add check to see if the instalocker was stopped successfully and return a descriptive value. Also add logging
    log.info('Instalocker stopped')
    return ''
