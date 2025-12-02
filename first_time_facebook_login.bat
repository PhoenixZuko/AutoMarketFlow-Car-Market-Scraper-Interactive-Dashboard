@echo off
set CHROME_PROFILE=C:\FB_Profile_HD

:: Verificăm dacă Chrome este instalat
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    set CHROME_PATH="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
) else (
    echo ❌ Google Chrome is not installed!
    pause
    exit /b
)

:: Deschidem profilul folosit de Selenium
echo 🚀 Opening Facebook profile used by Selenium...
start "" %CHROME_PATH% --user-data-dir=%CHROME_PROFILE% --profile-directory=Default https://www.facebook.com

exit
