ACTIVATE_VENV = cd .venv/Scripts & activate.bat & cd ../.. &


# Creates python virtual environment and install the requirements
.venv:
	python -m venv .venv --upgrade-deps
	$(ACTIVATE_VENV) pip install -r requirements.txt


# Install the requirements of the requirements.txt in the virtual environment
# It will only (re)install (the requirements are already installed on the .venv creation) the requirements if requirements.txt is newer than SITE_PACKAGES location (this means that the requirements.txt has been updated).
.PHONY: requirements
requirements: .venv\Lib\site-packages
.venv\Lib\site-packages: requirements.txt
	$(ACTIVATE_VENV) pip install -r requirements.txt


.PHONY: clean
clean:
	$(ACTIVATE_VENV) pyclean .


# Run the flask server and application
FLASK_ENVIRONMENT = development
# Check if the environment is valid
ifeq (,$(filter $(FLASK_ENVIRONMENT),development testing production))
    override FLASK_ENVIRONMENT = development
endif
# If FLASK_DEBUG is "" (nothing) the "--debug" flag will not be passed to the flask command.
FLASK_DEBUG =
ifeq ($(FLASK_DEBUG),on)
    override FLASK_DEBUG = --debug
else
    override FLASK_DEBUG =
endif
.PHONY: run_flask
run_flask:
	$(ACTIVATE_VENV) flask --app src.flask_application.app:create_app('$(FLASK_ENVIRONMENT)') $(FLASK_DEBUG) run


# Run the desktop file
.PHONY: run_desktop
run_desktop:
	$(ACTIVATE_VENV) python src/desktop.pyw


# Run the project tests 
.PHONY: run_tests
run_tests:
	$(ACTIVATE_VENV) pytest -c tests/pytest.ini
