@echo off
echo ============================================================
echo  Starting Streaming Voice Assistant
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Installing dependencies (if needed)...
pip install websockets flask-socketio python-socketio >nul 2>&1

echo.
echo ============================================================
echo  Starting server...
echo ============================================================
echo.
echo Server will be available at: http://localhost:5002
echo.
echo Features:
echo   - Real-time streaming responses
echo   - Interrupt with STOP button or ESC key
echo   - Push-to-talk (hold SPACE or button)
echo   - Conversation history
echo.
echo Press Ctrl+C to stop the server
echo.
echo ============================================================
echo.

python streaming_server.py

pause
