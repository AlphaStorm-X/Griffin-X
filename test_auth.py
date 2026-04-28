import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_auth_flow():
    print("--- Testing Authentication Flow ---")
    
    # 1. Register
    reg_payload = {
        "name": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    print(f"Registering user: {reg_payload['name']}...")
    res = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
    print(f"Status: {res.status_code}, Body: {res.json()}")

    # 2. Login
    print("\nLogging in...")
    login_payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    res = requests.post(f"{BASE_URL}/auth/login", data=login_payload)
    if res.status_code != 200:
        print(f"Login failed: {res.text}")
        return
    
    tokens = res.json()
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    print(f"Login successful. Access Token received (length: {len(access_token)})")

    # 3. Access Protected Route (Medicines)
    print("\nAccessing protected /api/medicines/...")
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{BASE_URL}/medicines/", headers=headers)
    print(f"Status: {res.status_code}, Medicines count: {len(res.json())}")

    # 4. Refresh Token
    print("\nRefreshing token...")
    res = requests.post(f"{BASE_URL}/auth/refresh?refresh_token={refresh_token}")
    if res.status_code == 200:
        new_tokens = res.json()
        print("Token refresh successful.")
    else:
        print(f"Token refresh failed: {res.text}")

if __name__ == "__main__":
    test_auth_flow()
