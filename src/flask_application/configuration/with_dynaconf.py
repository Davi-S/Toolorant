from dynaconf import FlaskDynaconf


def init_app(app, environment):
    FlaskDynaconf(app,
                  settings_files=['src/flask_application/settings.toml',
                                  'src/flask_application/.secrets.toml'],
                  extensions_list="EXTENSIONS",
                  ENV=environment)
