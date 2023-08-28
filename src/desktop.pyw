# Use pywebview to create desktop application
import webview
from flask_application.app import create_app

server = create_app('desktop')
webview.create_window('Toolorant', server)
webview.start()