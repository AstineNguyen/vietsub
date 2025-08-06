@echo off
echo.
echo ===================================================
echo    🎬 Enhanced Video Subtitle Tool V2
echo ===================================================
echo    Chinese Audio + OCR → Vietnamese Subtitles
echo ===================================================
echo.

cd /d "%~dp0"

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo    Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check if main file exists
if not exist "enhanced_video_subtitle_tool_v2.py" (
    echo ❌ Main application file not found!
    echo    Make sure enhanced_video_subtitle_tool_v2.py is in this folder.
    echo.
    pause
    exit /b 1
)

echo 🚀 Starting Enhanced Video Subtitle Tool V2...
echo.
python enhanced_video_subtitle_tool_v2.py

if errorlevel 1 (
    echo.
    echo ❌ Error occurred! Check the error message above.
    echo    Common solutions:
    echo    1. Install dependencies: pip install -r requirements.txt
    echo    2. Check internet connection
    echo    3. Make sure FFmpeg is installed
    echo.
    pause
) else (
    echo.
    echo ✅ Tool closed successfully.
    timeout /t 2 >nul
) 