@echo off
echo ============================================================
echo  Pushing Personal Jarvis to GitHub
echo ============================================================
echo.

cd /d "%~dp0"

echo Initializing git repository...
git init

echo.
echo Adding files...
git add .

echo.
echo Committing...
git commit -m "Initial commit: Personal Jarvis voice assistant with n8n integration"

echo.
echo Adding remote repository...
git remote add origin https://github.com/mchivelli/personal-jarvis.git

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main --force

echo.
echo ============================================================
echo  Done! Repository pushed to GitHub
echo ============================================================
echo.
echo You can now clone on your other machine:
echo   git clone https://github.com/mchivelli/personal-jarvis.git
echo.
pause
