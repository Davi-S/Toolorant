ACTIVATE_VENV = cd .venv/Scripts & activate.bat & cd ../.. &

.venv/: requirements.txt
	python -m venv .venv --upgrade-deps & \
	$(ACTIVATE_VENV) pip install -r requirements.txt

.PHONY: main
main: .venv/
	$(ACTIVATE_VENV) cd src/ & python Toolorant.py

.PHONY: designer
designer: .venv/
	$(ACTIVATE_VENV) pyside6-designer

.PHONY: exe
exe: .venv/
	$(ACTIVATE_VENV) nuitka --standalone --remove-output --disable-console \
	--windows-icon-from-ico="src/resources/favicon.ico" \
	--plugin-enable=pyside6 \
	--include-package=websockets \
	--include-data-files=src/view/*.qss=view/ \
	--include-data-files=src/settings/*.toml=settings/ \
	--include-data-files=src/settings/*.json=settings/ \
	src/Toolorant.py