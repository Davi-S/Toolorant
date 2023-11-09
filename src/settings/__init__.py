import json
from pathlib import Path

import dynaconf

APP_SETTINGS_PATH = Path(__file__).resolve().parent / 'app_settings.toml'
USER_SETTINGS_PATH = Path(__file__).resolve().parent / 'user_settings.json'
SECRETS_PATH = Path(__file__).resolve().parent / '.secrets.toml'


class CustomDynaconf(dynaconf.Dynaconf):
    """Dynaconf class with method to save the changed settings"""

    def persist(self):
        # https://www.dynaconf.com/advanced/#exporting
        # loaders.write(self['SETTINGS_FILE_FOR_DYNACONF'][0], self.to_dict())
        with open(self['SETTINGS_FILE_FOR_DYNACONF'][0], 'w') as file:
            json.dump(self.to_dict(), file, indent=4)


app_settings = dynaconf.Dynaconf(
    settings_files=[
        APP_SETTINGS_PATH,
        SECRETS_PATH
    ]
)

user_settings = CustomDynaconf(
    settings_files=[
        USER_SETTINGS_PATH
    ]
)
