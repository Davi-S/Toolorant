import importlib
import json

import dynaconf
import flask
import toml


class CustomDynaconf(dynaconf.Dynaconf):
    def persist(self):
        # https://www.dynaconf.com/advanced/#exporting
        # loaders.write(self['SETTINGS_FILE_FOR_DYNACONF'][0], self.to_dict())
        with open(self['SETTINGS_FILE_FOR_DYNACONF'][0], 'w') as json_file:
            # Use indent for formatting
            json.dump(self.to_dict(), json_file, indent=4)


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
    file_config = load_toml('config/settings.toml')
    app.config.update(file_config)
    app.logger.info('Configurations loaded')
    # User settings
    app.user_settings = CustomDynaconf(
        settings_files=['config/user_settings.json']
    )
    app.logger.info('User settings loaded')
    # Extensions
    load_extensions(app, app.config.get('EXTENSIONS'))
    app.logger.info('Extensions loaded')
