@echo off
setlocal
echo ===================================================
echo   Amana Capital - Fetch Historical DSE Report
echo ===================================================
echo.

cd /d "C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
"C:\Users\tmalu\AppData\Local\Programs\Python\Python312\python.exe" fetch_historical_dse.py

echo.
echo Process complete!
pause
