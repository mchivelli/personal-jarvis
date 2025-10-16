@echo off
echo ============================================================
echo  Pushing Personal Jarvis to GitHub
echo ============================================================
echo.

cd /d "%~dp0"

echo Step 1: Adding files...
git add .

echo.
echo Step 2: Committing...
git commit -m "Personal Jarvis voice assistant"

echo.
echo Step 3: Adding remote repository...
git remote add origin https://github.com/mchivelli/personal-jarvis.git 2>nul
if errorlevel 1 (
    echo Remote already exists, updating...
    git remote set-url origin https://github.com/mchivelli/personal-jarvis.git
)

echo.
echo Step 4: Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ============================================================
echo  Done! Repository pushed to GitHub
echo ============================================================
echo.
echo You can now clone on your other machine:
echo   git clone https://github.com/mchivelli/personal-jarvis.git
echo.
echo Remember to:
echo 1. Update .env with your n8n server address
echo 2. Install Python dependencies: pip install -r requirements.txt
echo 3. Test webhook connectivity
echo.
pause
