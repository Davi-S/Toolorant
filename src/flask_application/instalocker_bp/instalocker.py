# TODO: The fact that the profile can be None is bad because it add a lot of checking. Need to find a way to reduce the amount of checks
import flask
from .instalocker_cls import Instalocker
from .profile import Profile, get_all_profiles
from .. import forms
from .. import game_resources as gr


instalocker_bp = flask.Blueprint('instalocker_bp', __name__,
                                 template_folder='templates')


def init_app(app: flask.Flask):
    # Create and configure instalocker
    instalocker = Instalocker()
    profile_name = app.user_settings.profile
    instalocker.profile = None if profile_name is None else Profile.load(profile_name)

    instalocker_bp.instalocker = instalocker
    app.register_blueprint(instalocker_bp, url_prefix='/instalocker')


@instalocker_bp.route('/', methods=['GET', 'POST'])
def index():
    # TODO: Check bug where submitting the select_form without fields makes the create_form show errors
    ##### SELECT PROFILE FORM #####
    profiles = [profile.name for profile in get_all_profiles()]
    user_profile = instalocker_bp.instalocker.profile
    select_profile_form = forms.SelectProfiles(profiles,
                                               None if user_profile is None
                                               else profiles.index(user_profile.name))
    if select_profile_form.validate_on_submit():
        # Passing the current app as argument
        if select_profile_form.set.data:
            set_profile(select_profile_form.profile_name.data)

        elif select_profile_form.delete.data:
            delete_profile(select_profile_form.profile_name.data)

        return flask.redirect(flask.url_for('instalocker_bp.index'))
    # Process the form to "reconstruct" the html with the radio default ("checked").
    # Must be called after the validate_on_submit
    select_profile_form.process()

    ##### CREATE PROFILE FORM #####
    new_profile_form = forms.NewProfileInfo()
    if new_profile_form.validate_on_submit():
        create_profile(new_profile_form)
        return flask.redirect(flask.url_for('instalocker_bp.index'))

    return flask.render_template('instalocker/index.html',
                                 select_profile_form=select_profile_form,
                                 new_profile_form=new_profile_form)


def set_profile(profile_name):
    # Set the profile on the instalocker and on the user settings
    instalocker_bp.instalocker.profile = Profile.load(profile_name)
    flask.current_app.user_settings.profile = profile_name
    flask.current_app.user_settings.persist()


def delete_profile(profile_name):
    # Create a profile object
    profile = Profile.load(profile_name)
    # Delete the profile file
    Profile.delete(profile.name)
    # Check if the profile deleted was set on the instalocker and/or user settings and remove its references
    if instalocker_bp.instalocker.profile == profile:
        instalocker_bp.instalocker.profile = None
    if flask.current_app.user_settings.profile == profile.name:
        flask.current_app.user_settings.profile = None


def create_profile(form: forms.NewProfileInfo):
    profile_info = {'name': form.name.data,
                    'game_mode': gr.GameMode[form.game_mode.data.upper()],
                    'map_agent': {gr.Map[field_name.upper()]: gr.Agent[field.data.upper()] if field.data.upper() != 'NONE' else None
                                  for field_name, field in form._fields.items()
                                  if field_name.upper() in [en.name for en in gr.Map]}}
    Profile(profile_info['name'],
            profile_info['game_mode'],
            profile_info['map_agent']).dump()


# TODO: save state on the session to pass it to the page and load with the checkbox on/off
@instalocker_bp.route('/start', methods=['POST'])
def start():
    flask.current_app.websocket.add_listener(instalocker_bp.instalocker)
    return ''


@instalocker_bp.route('/stop', methods=['POST'])
def stop():
    flask.current_app.websocket.remove_listener(instalocker_bp.instalocker)
    return ''
