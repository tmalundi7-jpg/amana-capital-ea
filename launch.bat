@echo off
setlocal
echo ===================================================
echo   Amana Capital - Daily Website Update Launcher
echo ===================================================
echo.
set "BASE_DIR=C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
cd /d "%BASE_DIR%"

powershell -NoProfile -ExecutionPolicy Bypass -File "launch_helper.ps1"
if %ERRORLEVEL% neq 0 (
    echo.
    echo Please save today's files in the Documents folder and try again.
    pause
    exit /b 1
)

echo.
echo Launching automated instructions into Antigravity...
cscript //nologo auto_paste.vbs

echo Process complete! You can close this window.
timeout /t 3 >nul
