from dynaconf import Dynaconf, loaders


class CustomDynaconf(Dynaconf):
    def persist(self):
        loaders.write(self['SETTINGS_FILE_FOR_DYNACONF'][0], self.to_dict())


def init_app(app):
    app.user_settings = CustomDynaconf(
        settings_files=['src/flask_application/user_settings.json'])
