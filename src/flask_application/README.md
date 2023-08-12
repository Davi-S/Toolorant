TODO: improve this readme
# Brief Folder information
This folder contains the project Flask application.


# How to run
To start the server, on the root directory run:
```
$ make run_flask
```
This will start the app in development mode and with debug mode off.

You can add the following arguments:
- `FLASK_ENVIRONMENT` to change the environment. Valid values are: "development", "testing" or "production".

    Example: `$ make run_flask FLASK_ENVIRONMENT=testing`
- `FLASK_DEBUG=on` to activate the debug mode.

    Example: `$ make run_flask FLASK_DEBUG=on`


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