cd /D "%~dp0"
CALL env\Scripts\activate.bat
start "" http://127.0.0.1:8000/
python manage.py runserver