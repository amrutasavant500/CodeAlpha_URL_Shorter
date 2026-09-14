@echo off
echo Installing required package...
python -m pip install -r requirements.txt
echo.
echo Starting URL Shortener...
python app.py
pause
