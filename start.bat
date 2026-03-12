@echo off
echo ========================================
echo Starting HealthSecure Dashboard
echo ========================================
echo.

echo [1/4] Checking MongoDB connection...
python -c "from backend.database import db; print('MongoDB connected!')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: MongoDB is not running!
    echo Please start MongoDB first, then run this script again.
    pause
    exit /b 1
)
echo.

echo [2/4] Seeding database...
python backend\seed.py
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to seed database. Continuing anyway...
)
echo.

echo [3/4] Starting Backend on port 8001 (with auto-reload)...
start "Backend Server" cmd /k "cd /d c:\Users\eh722\OneDrive - presidencyuniversity.in\Desktop\healthsecure-dashboard && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload"
echo.

echo [4/4] Starting Frontend...
start "Frontend Server" cmd /k "cd /d c:\Users\eh722\OneDrive - presidencyuniversity.in\Desktop\healthsecure-dashboard\frontend\my-app && npm start"
echo.

echo ========================================
echo All servers starting!
echo - Backend: http://localhost:8001
echo - Frontend: http://localhost:3000
echo.
echo NOTE: Wait a few seconds for servers to start, then refresh your browser.
echo ========================================
pause
