@echo off

cd..
python38\python -m venv env

copy hacer_portable\activate.bat env\scripts\activate.bat /y
copy hacer_portable\requirements.txt . /y
call env\scripts\activate.bat

python -m pip install  --upgrade pip --user
python -m pip install -r requirements.txt

pause