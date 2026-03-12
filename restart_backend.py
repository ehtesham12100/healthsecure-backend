import subprocess
import time
import signal
import os

# Change to project directory
os.chdir(r"c:\Users\eh722\OneDrive - presidencyuniversity.in\Desktop\healthsecure-dashboard")

# Find and kill existing uvicorn process on port 8001
try:
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if ':8001' in line and 'LISTENING' in line:
            pid = line.split()[-1]
            print(f"Killing process {pid} on port 8001")
            subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
            time.sleep(1)
except Exception as e:
    print(f"Error finding process: {e}")

# Start new server with reload
print("Starting backend with auto-reload...")
proc = subprocess.Popen(
    ['python', '-m', 'uvicorn', 'backend.main:app', '--host', '127.0.0.1', '--port', '8001', '--reload'],
    cwd=r"c:\Users\eh722\OneDrive - presidencyuniversity.in\Desktop\healthsecure-dashboard"
)

print(f"Backend started with PID: {proc.pid}")
print("Server running at http://127.0.0.1:8001")
print("Press Ctrl+C to stop")

try:
    proc.wait()
except KeyboardInterrupt:
    print("\nStopping server...")
    proc.terminate()
