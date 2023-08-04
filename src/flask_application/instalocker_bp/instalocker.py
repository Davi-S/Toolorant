# TODO: The fact that the profile can be None is bad because it adds a lot of checking. Need to find a way to reduce the amount of checks for this
# TODO: Add feature to set a delay on selecting and locking the character to prevent account suspension
import flask

from .. import forms
from .. import game_resources as gr
from .instalocker_cls import Instalocker
from .profile import Profile, get_all_profiles


instalocker_bp = flask.Blueprint('instalocker_bp', __name__,
                                 template_folder='templates')


def init_app(app: flask.Flask):
    # Create and configure instalocker
    instalocker = Instalocker(app.client)
    profile_name = app.user_settings.profile
    instalocker.profile = None if profile_name is None else Profile.load(profile_name)

    instalocker_bp.instalocker = instalocker
    app.register_blueprint(instalocker_bp, url_prefix='/instalocker')


@instalocker_bp.route('/', methods=['GET', 'POST'])
def index():
    return flask.render_template('instalocker/index.html',
                                 profiles=get_all_profiles(),
                                 selected_profile=instalocker_bp.instalocker.profile,
                                 instalocker_active=flask.session.get('instalocker_active', False),
                                 new_profile_form=forms.NewProfileInfo())


@instalocker_bp.route('/set', methods=['POST'])
def set_profile():
    profile_name = flask.request.form.get('profile_name')
    # Set the profile on the instalocker and on the user settings
    instalocker_bp.instalocker.profile = Profile.load(profile_name)
    flask.current_app.user_settings.profile = profile_name
    flask.current_app.user_settings.persist()
    return ''


@instalocker_bp.route('/delete', methods=['POST'])
def delete_profile():
    profile_name = flask.request.form.get('profile_name')
    # Create a profile object for comparison
    profile = Profile.load(profile_name)
    # Delete the profile file
    Profile.delete(profile_name)
    # Check if the profile deleted was set on the instalocker and/or user settings and remove its references
    if instalocker_bp.instalocker.profile == profile:
        instalocker_bp.instalocker.profile = None
    if flask.current_app.user_settings.profile == profile.name:
        flask.current_app.user_settings.profile = None
        flask.current_app.user_settings.persist()
    return ''


@instalocker_bp.route('/create', methods=['POST'])
def create_profile():
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
    return ''


@instalocker_bp.route('/start', methods=['POST'])
def start():
    flask.current_app.websocket.add_listener(instalocker_bp.instalocker)
    flask.session['instalocker_active'] = True
    return ''


@instalocker_bp.route('/stop', methods=['POST'])
def stop():
    flask.current_app.websocket.remove_listener(instalocker_bp.instalocker)
    flask.session["instalocker_active"] = False
    return ''
