@echo off

set ENV_NAME=myenv
set REQUIREMENTS_FILE=requirements.txt
set PY_FILE_NAME=main.py

echo Creating virtual environment...
python -m venv %ENV_NAME%

echo Activating virtual environment...
call %ENV_NAME%\Scripts\activate.bat

echo Installing requirements...
pip install -r %REQUIREMENTS_FILE%

echo Running python script
py %PY_FILE_NAME%

echo Done.