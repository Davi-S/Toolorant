# TODO: add option to pass command line arguments to create the flask app with other environments and set logging levels
# Set python root directory
import sys
import os
import pathlib
current_script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
root_directory = pathlib.Path(current_script_directory).parent.absolute()
os.chdir(root_directory)

# Setup logging
import logging
import logging.config
from logging_configuration import CONFIG_DICT, create_file_handler
logging.config.dictConfig(CONFIG_DICT)

# IMPORTS
import webview

from flask_application.app import create_app

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))

# Use pywebview to create desktop application
server = create_app('desktop')
webview.create_window('Toolorant', server, width=1200, height=720)
webview.start()