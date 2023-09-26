import logging

import flask

import game_resources as gr

from . import forms
from .profile import Profile, get_all_profiles


logger = logging.getLogger(__name__)

instalocker_bp = flask.Blueprint('instalocker',
                                 __name__,
                                 template_folder='templates')


@instalocker_bp.route('/')
def index():
    return flask.render_template(
        'instalocker/instalocker.html',
        profiles=get_all_profiles(),
        selected_profile=instalocker_bp.instalocker.profile,
        instalocker_active=flask.session.get('instalocker_active', False),
        new_profile_form=forms.NewProfileInfo(),
        select_delay=flask.current_app.user_settings.instalocker.select_delay,
        lock_delay=flask.current_app.user_settings.instalocker.lock_delay
    )


@instalocker_bp.route('/set', methods=['PUT'])
def set_profile():
    try:
        profile_name = flask.request.form.get('profile_name')
        # Set the profile on the instalocker and on the user settings
        instalocker_bp.instalocker.profile = Profile.load(profile_name)
        flask.current_app.user_settings.instalocker.profile = profile_name
        flask.current_app.user_settings.persist()
        logger.info(f'Profile "{profile_name}" set successfully')
        return flask.jsonify(True)
    except Exception as e:
        logger.error(f'Error occurred while setting the profile "{profile_name}". Error: {e}')
        return flask.jsonify(False)


@instalocker_bp.route('/delete', methods=['DELETE'])
def delete_profile():
    try:
        profile_name = flask.request.form.get('profile_name')
        profile = Profile.load(profile_name)
        # Check if the profile was set on the instalocker and/or user settings and remove its references if needed
        if instalocker_bp.instalocker.profile == profile:
            instalocker_bp.instalocker.profile = None
        if flask.current_app.user_settings.instalocker.profile == profile.name:
            flask.current_app.user_settings.instalocker.profile = None
            flask.current_app.user_settings.persist()
        profile.delete()
        logger.info(f'Profile "{profile_name}" deleted successfully')
        return flask.jsonify(True)
    except Exception as e:
        logger.error(f'Error occurred while deleting the profile "{profile_name}". Error: {e}')
        return flask.jsonify(False)     


@instalocker_bp.route('/create', methods=['POST'])
def create_profile():
    try:
        form = forms.NewProfileInfo()
        profile_info = {
            'name': form.name.data,
            # Dictionary comprehension to dynamically build the map-agent based on the game resources classes and field names.
            'map_agent': {
                gr.Map[field_name.upper()]: (gr.Agent[field.data.upper()] if field.data.upper() != 'NONE' else None)
                for field_name, field
                in form._fields.items()
                if field_name.upper() in [game_map.name for game_map in gr.Map]}
            }
        
        Profile(
            profile_info['name'],
            profile_info['map_agent']
        ).add()
        logger.info(f'Profile "{profile_info["name"]}" created successfully')
        return flask.jsonify(True)
    except Exception as e:
        logger.error(f'Error occurred while creating the profile "{profile_info["name"]}". Error: {e}')
        return flask.jsonify(False)


@instalocker_bp.route('/set-select-delay', methods=['PUT'])
def set_select_delay():
    try:
        select_delay = int(flask.request.form.get('delay'))
        instalocker_bp.instalocker.select_delay = select_delay
        flask.current_app.user_settings.instalocker.select_delay = select_delay
        flask.current_app.user_settings.persist()
        logger.info(f'Select delay "{select_delay}" set successfully')
        return flask.jsonify(True)
    except Exception as e:
        logger.error(f'Error occurred while setting the select delay "{select_delay}". Error: {e}')
        return flask.jsonify(False)   


@instalocker_bp.route('/set-lock-delay', methods=['PUT'])
def set_lock_delay():
    try:
        lock_delay = int(flask.request.form.get('delay'))
        instalocker_bp.instalocker.lock_delay = lock_delay
        flask.current_app.user_settings.instalocker.lock_delay = lock_delay
        flask.current_app.user_settings.persist()
        logger.info(f'Lock delay "{lock_delay}" set successfully')
        return flask.jsonify(True)   
    except Exception as e:
        logger.error(f'Error occurred while setting the lock delay "{lock_delay}". Error: {e}')
        return flask.jsonify(False)   


@instalocker_bp.route('/start', methods=['PUT'])
def start():
    try:
        flask.current_app.websocket.add_listener(instalocker_bp.instalocker)
        flask.session['instalocker_active'] = True
        logger.info('Instalocker started successfully')
        return flask.jsonify(True)
    except Exception as e:
        logger.error(f'Error occurred while starting the instalock. Error: {e}')
        return flask.jsonify(False)


@instalocker_bp.route('/stop', methods=['PUT'])
def stop():
    try:
        flask.current_app.websocket.remove_listener(instalocker_bp.instalocker)
        flask.session["instalocker_active"] = False
        logger.info('Instalocker stopped successfully')
        return flask.jsonify(True)
    except Exception as e:
        logger.error(f'Error occurred while stopping the instalock. Error: {e}')
        return flask.jsonify(False)
