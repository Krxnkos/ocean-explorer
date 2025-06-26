@echo off
echo Starting Ocean Explorer...

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH! Please install Python 3.x
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking requirements...
pip install -r requirements.txt > nul 2>&1

REM Run the game
echo Launching game...
python -m src.core.game

pause