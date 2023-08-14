@echo off
echo Creating and upgrading virtual environment...
python -m venv .venv --upgrade-deps

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo All commands executed successfully.