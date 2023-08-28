# Use pywebview to create desktop application
# Setup logging first
import logging
import logging.config
from logging_configuration import CONFIG_DICT, create_file_handler
logging.config.dictConfig(CONFIG_DICT)

import webview

from flask_application.app import create_app

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

server = create_app('desktop')
webview.create_window('Toolorant', server, width=1200)
webview.start()