@echo off
echo ================================================
echo  Starting Simple Voice Chat Server
echo ================================================
echo.
echo This server ONLY connects to remote n8n
echo No local Ollama or Whisper needed
echo.

REM Install dependencies if needed
echo Checking dependencies...
pip install -q flask flask-cors requests python-dotenv

echo.
echo Starting server...
echo Open http://localhost:5000 in your browser
echo.

python simple_server.py

pause
