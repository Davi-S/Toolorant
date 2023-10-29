ACTIVATE_VENV = cd .venv/Scripts & activate.bat & cd ../.. &

.PHONY: main
main:
	$(ACTIVATE_VENV) cd src/ & python Toolorant.py

.PHONY: designer
designer:
	$(ACTIVATE_VENV) pyside6-designer

.PHONY: exe_dir
exe_dir:
	$(ACTIVATE_VENV) pyinstaller --noconfirm --clean --noconsole \
	--distpath dist/dir \
	--icon "src/resources/favicon.ico" \
	--paths .venv/Lib/site-packages \
	--add-data "src/.logs;.logs/" \
	--add-data "src/settings;settings/" \
	--add-data "src/pages;pages/" \
	--add-data "src/view;view/" \
	src/Toolorant.py \

.PHONY: exe_file
exe_file:
	$(ACTIVATE_VENV) pyinstaller --noconfirm --clean --noconsole --onefile \
	--distpath dist/file \
	--icon "src/resources/favicon.ico" \
	--paths .venv\Lib\site-packages \
	--add-data "src/.logs;.logs/" \
	--add-data "src/settings;settings/" \
	--add-data "src/pages;pages/" \
	--add-data "src/view;view/" \
	src\Toolorant.py

.PHONY: exe_nuitka
exe_nuitka:
	$(ACTIVATE_VENV) nuitka --standalone --remove-output --disable-console \
	--windows-icon-from-ico="src/resources/favicon.ico" \
	--plugin-enable=pyside6 \
	--include-module=websockets \
	--include-data-files=src/view/*.qss=view/ \
	--include-data-files=src/settings/*.toml=settings/ \
	--include-data-files=src/settings/*.json=settings/ \
	src/Toolorant.py