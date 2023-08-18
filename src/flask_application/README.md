# Brief Folder information
This folder contains the project Flask application.

The project is based on Flask but it is not meant to be used as a web application, it is meant to be used as a desktop application, the Pywebview framework is used to transform the flask app into a desktop app (`src\desktop.py`).

The web project structure and design are used mainly because the GUI; is easier to work with and more people are already familiar with how web structure works.

# Basic start
If you have `Make` installed, run the following command on the root directory to start the server:
```
$ make run_flask
```

You can add the following arguments:
- `FLASK_ENVIRONMENT` to change the environment. Valid values are: "development", "testing" or "production".

    Example: `$ make run_flask FLASK_ENVIRONMENT=testing`
- `FLASK_DEBUG=on` to activate the debug mode.

    Example: `$ make run_flask FLASK_DEBUG=on`

*See the `Makefile` for the full command. Also see the flask documentation for more details*

# Folder Structure
Using a [divisional](https://stackoverflow.com/a/40553522/14593213) folder structure.

See the following example:

```
flask_application/
|
├── flask_blueprint_name/
|   ├── templates/
|   |   └── flask_blueprint_name/
|   |       ├── some_template1.html
|   |       └── ...
|   |
|   ├── static/
|   |   ├── blueprint.css
|   |   ├── blueprint.js
|   |   ├── some_image1.png
|   |   └── ...
|   |
|   ├── __init__.py
|   └── flask_blueprint_name.py
|
├── static/
|   ├── main.css
|   ├── main.js
|   ├── some_image.png
|   └── ...
|
├── templates/
|   ├── some_template1.html
|   └── ...
|
├── app.
├── settings.toml
├── README.md
├── __init__.py
└── ...
```

# Useful links
- [Divisional vs functional structure](https://stackoverflow.com/a/40553522/14593213)
- [Blueprint and file structure](https://realpython.com/flask-blueprint/)
- [Flask project structure architecture (using factory pattern)](https://www.youtube.com/watch?v=-qWySnuoaTM)
- [Flask patterns](https://flask.palletsprojects.com/en/2.2.x/patterns/)
- [Endpoints](https://stackoverflow.com/a/19262349/14593213)