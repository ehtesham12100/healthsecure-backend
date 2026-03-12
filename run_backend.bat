@echo off
cd /d c:\Users\eh722\OneDrive - presidencyuniversity.in\Desktop\healthsecure-dashboard
echo Starting HealthSecure Backend with auto-reload...
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
