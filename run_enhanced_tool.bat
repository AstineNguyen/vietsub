@echo off
title Enhanced Video Subtitle Tool
echo.
echo =============================================
echo    Enhanced Video Subtitle Tool - Starting
echo    Chinese Audio + Text Recognition
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if enhanced dependencies are installed
echo Checking dependencies...
python -c "import whisper, moviepy, googletrans, pysrt, pytesseract, cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting Enhanced Video Subtitle Tool...
echo Features:
echo - Chinese audio recognition
echo - Chinese text detection in video (OCR)
echo - Vietnamese translation
echo - Multiple export formats
echo - Video overlay options
echo.
python enhanced_video_subtitle_tool.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Tool exited with error code %errorlevel%
)

echo.
echo Press any key to exit...
pause >nul 