@echo off
cd /d %~dp0
title 🚀 AutoMarket Environment Setup

echo [1/4] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed.
    echo Please download it from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

echo [2/4] Checking for pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ⚡ Pip not found. Installing pip...
    python -m ensurepip
)

echo [3/4] Preparing the environment...
python setup_environment.py
if errorlevel 1 (
    echo ❌ Something went wrong during setup. Aborting launch.
    pause
    exit /b
)

echo [4/4] Launching dashboard and browser in a new terminal...

:: Create temporary script to run the dashboard
(
echo @echo off
echo cd /d %%~dp0
echo python dasboard.py
) > run_dashboard.bat

:: Launch dashboard in a new visible terminal
start "Dashboard" cmd /k run_dashboard.bat

:: Wait 3 seconds before launching the browser
timeout /t 3 >nul

:: Launch Chrome
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window http://127.0.0.1:5000
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --new-window http://127.0.0.1:5000
) else (
    echo ❌ Google Chrome not found! Please install it from https://www.google.com/chrome/
    pause
)

:: Clean up the temporary script
del /f /q run_dashboard.bat

:: Close this window
exit
