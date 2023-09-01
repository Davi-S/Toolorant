import logging

from dynaconf import Dynaconf, loaders

from logging_configuration import create_file_handler

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

class CustomDynaconf(Dynaconf):
    def persist(self):
        # https://www.dynaconf.com/advanced/#exporting
        loaders.write(self['SETTINGS_FILE_FOR_DYNACONF'][0], self.to_dict())


def init_app(app):
    app.user_settings = CustomDynaconf(
        settings_files=['src/flask_application/user_settings/user_settings.json'])
    log.info('User settings loaded')
