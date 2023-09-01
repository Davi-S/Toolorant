import logging

from dynaconf import FlaskDynaconf

from logging_configuration import create_file_handler


# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

def init_app(app, environment):
    FlaskDynaconf(app,
                  settings_files=['src/flask_application/settings.toml',
                                  'src/flask_application/.secrets.toml'],
                  extensions_list="EXTENSIONS",
                  ENV=environment)
    log.info('FlaskDynaconf object created successfully')   
