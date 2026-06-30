@echo off
:: Dukan Windows EXE Builder
:: This script compiles the Python backend into a standalone Windows EXE
:: Requires: Python, pip, pyinstaller
::
:: NOTE: This EXE is for LOCAL TESTING ONLY with ngrok
:: For production, deploy to a cloud server (Render, Railway, etc.)

@echo on

echo ============================================
echo  DUKAN - Windows EXE Builder
echo ============================================
echo.

:: Check if Python is installed
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)
echo Python found: %python --version%
echo.

:: Install pyinstaller
echo [2/5] Installing PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: Failed to install pyinstaller
    pause
    exit /b 1
)
echo.

:: Install dependencies
echo [3/5] Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

:: Initialize database
echo [4/5] Initializing database...
python main.py --init-db
if errorlevel 1 (
    echo WARNING: Database initialization may have failed
)
echo.

:: Build EXE
echo [5/5] Building EXE (this may take a few minutes)...
echo.
pyinstaller --onefile --windowed --name DukanBot --icon=NONE main.py
if errorlevel 1 (
    echo ERROR: Failed to build EXE
    pause
    exit /b 1
)
echo.

echo ============================================
echo  SUCCESS! EXE created in dist/DukanBot.exe
echo ============================================
echo.
echo IMPORTANT NOTES:
echo 1. This EXE is for LOCAL TESTING ONLY
echo 2. You MUST run ngrok to expose it to the internet
echo 3. For production, deploy to a cloud server
echo.
echo To run:
echo   1. Start ngrok: ngrok http 8000
echo   2. Set WEBHOOK_URL in .env to your ngrok URL
echo   3. Run: dist/DukanBot.exe
echo.
echo For production deployment, see CLOUD_DEPLOY.md
echo.
pause
