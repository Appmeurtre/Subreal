@echo off
title Subreal Engine Console GUI
color 0E

echo.
echo ========================================
echo   Subreal Engine Console GUI
echo ========================================
echo Starting application...
echo.

:: Change to the script directory
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    echo Visit: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check if the main script exists
if not exist "subreal_gui.py" (
    echo ERROR: subreal_gui.py not found in current directory
    echo Make sure you're running this from the correct folder
    echo.
    pause
    exit /b 1
)

:: Run the Python GUI
python subreal_gui.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
) else (
    echo.
    echo Application closed normally.
    timeout /t 2 /nobreak >nul
)