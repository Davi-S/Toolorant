import importlib
import json
from pathlib import Path

import dynaconf
import flask
import toml


SETTINGS_PATH = Path(__file__).resolve().parent / 'settings.toml'
USER_SETTINGS_PATH = Path(__file__).resolve().parent / 'user_settings.json'

class CustomDynaconf(dynaconf.Dynaconf):
    def persist(self):
        # https://www.dynaconf.com/advanced/#exporting
        # loaders.write(self['SETTINGS_FILE_FOR_DYNACONF'][0], self.to_dict())
        with open(self['SETTINGS_FILE_FOR_DYNACONF'][0], 'w') as file:
            json.dump(self.to_dict(), file, indent=4)


def load_toml(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        config = toml.load(file)
    return config


def load_extensions(app, extensions_list):
    for extension in extensions_list:
        extension_module, init_function = extension.split(':')
        ext = importlib.import_module(extension_module)
        getattr(ext, init_function)(app)


def init_app(app: flask.Flask):
    # Flask settings
    file_config = load_toml(SETTINGS_PATH)
    app.config.update(file_config)
    app.logger.info('Configurations loaded')
    # User settings
    app.user_settings = CustomDynaconf(
        settings_files=[USER_SETTINGS_PATH]
    )
    app.logger.info('User settings loaded')
    # Extensions
    load_extensions(app, app.config.get('EXTENSIONS'))
    app.logger.info('Extensions loaded')
