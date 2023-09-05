# Set python root directory
import sys
import os
import pathlib
current_script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
root_directory = pathlib.Path(current_script_directory).parent.absolute()
os.chdir(root_directory)

from flask_application.app import create_app

app = create_app()
app.run(debug=True)