@echo off
title Video Subtitle Tool
echo.
echo ====================================
echo    Video Subtitle Tool - Starting
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import whisper, moviepy, googletrans, pysrt" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting Video Subtitle Tool...
echo.
python video_subtitle_tool.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Tool exited with error code %errorlevel%
)

echo.
echo Press any key to exit...
pause >nul 