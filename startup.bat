@echo off
REM startup.bat - For local Windows testing (Single Process)

REM Set default port
if not defined PORT set PORT=8000

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run the application
echo Starting Car Price Predictor on port %PORT%...
python main.py

pause
