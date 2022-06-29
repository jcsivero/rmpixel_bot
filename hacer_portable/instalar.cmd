rem @echo off

python38\python -m venv env
call env\scripts\activate

rem python -m pip install  --upgrade pip --user
python -m pip install -r requirements.txt

pause