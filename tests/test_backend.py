import requests

# Test root endpoint
response = requests.get("http://127.0.0.1:8001/")
print(f"Root endpoint: {response.status_code} - {response.json()}")

# Test login endpoint
login_data = {"username": "admin", "password": "admin123"}
response = requests.post("http://127.0.0.1:8001/auth/login", json=login_data)
print(f"Login endpoint: {response.status_code} - {response.json()}")
