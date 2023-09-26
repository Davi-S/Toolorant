ACTIVATE_VENV = cd .venv/Scripts & activate.bat & cd ../.. &

.PHONY: run
run:
	$(ACTIVATE_VENV) cd src/ && python toolorant.py

.PHONY: run_flask
run_flask:
	$(ACTIVATE_VENV) cd src/ && flask run

.PHONY: exe_dir
exe_dir:
	$(ACTIVATE_VENV) pyinstaller --noconfirm --clean --noconsole \
	--icon "assets\logo2.ico" \
	--paths .venv\Lib\site-packages \
	--add-data "src/config;config" \
	--add-data "src/blueprints;blueprints" \
	--add-data "src/extensions;extensions" \
	--add-data "src/static;static" \
	--add-data "src/templates;templates" \
	--add-data "src/abstracts.py:." \
	--add-data "src/forms.py:." \
	--add-data "src/game_resources.py:." \
	--hidden-import valclient \
	--hidden-import websockets \
	--hidden-import flask_wtf \
	src\toolorant.py

.PHONY: exe_file
exe_file:
	$(ACTIVATE_VENV) pyinstaller --noconfirm --clean --noconsole --onefile \
	--distpath dist/file \
	--icon "assets\logo2.ico" \
	--paths .venv\Lib\site-packages \
	--add-data "src/config;config" \
	--add-data "src/blueprints;blueprints" \
	--add-data "src/extensions;extensions" \
	--add-data "src/static;static" \
	--add-data "src/templates;templates" \
	--add-data "src/abstracts.py:." \
	--add-data "src/forms.py:." \
	--add-data "src/game_resources.py:." \
	--hidden-import valclient \
	--hidden-import websockets \
	--hidden-import flask_wtf \
	src\toolorant.py
