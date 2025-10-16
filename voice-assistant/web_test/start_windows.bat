@echo off
echo ============================================================
echo  Voice Assistant Web Test - Windows
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Set environment variables
set N8N_WEBHOOK_URL=http://172.22.32.1:32768/webhook/voice-assistant
set WHISPER_MODEL=base.en

echo Starting Voice Assistant Web Server...
echo.
echo n8n Webhook: %N8N_WEBHOOK_URL%
echo Whisper Model: %WHISPER_MODEL%
echo.
echo Server will start at: http://localhost:5000
echo.

REM Start the server
python server_windows.py

pause
