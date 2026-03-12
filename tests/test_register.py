import requests

# Test registration endpoint
response = requests.post(
    'http://localhost:8001/auth/register',
    json={
        'username': 'testuser3',
        'email': 'test3@test.com',
        'password': 'test123'
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
