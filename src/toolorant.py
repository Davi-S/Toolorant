print('===== Called "toolorant.py" file =====')
print('===== Starting logging configuration =====')
# SETUP LOGGING
import logging
import logging.config
from config.logging_config import dict_config
logging.config.dictConfig(dict_config)
print('===== Finished logging configuration =====')

print('===== Starting imports =====')
# IMPORTS
import webview
import app
print('===== Finished imports =====')

print('===== Starting main code =====')
flask_app = app.create_app()
webview.create_window('Toolorant', flask_app, width=1200, height=650, min_size=(1050, 650))
webview.start()
print('===== Finished main code =====')
print('===== Exiting "toolorant.py" file =====')