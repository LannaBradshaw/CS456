import time, requests

MAX_CRASH_ATTEMPTS = 100
BASE_URL = "http://127.0.0.1:5555"
token = requests.post(f"{BASE_URL}/login", json={"username": "admin", "password": "password123"}).json()["token"]

for _ in range(MAX_CRASH_ATTEMPTS):
    try:
        requests.post(f"{BASE_URL}/login", json={"username": "?", "password": "?"}, timeout=1)
    except requests.RequestException:
        print("Fault successfully triggered")
        break
    time.sleep(0.02)

time.sleep(3)

print(requests.get(f"{BASE_URL}/session", params={"token": token}).json())

