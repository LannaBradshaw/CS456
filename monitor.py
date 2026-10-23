import time

import requests

online = False
failures = 0


def get_status():
    try:
        response = requests.get("http://localhost:5555/status")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        # print(f"Error occurred: {e}")
        return False


online = get_status()
print(f"Initial status: Server is {'Online' if online else 'Offline'}")

while True:
    init_status = online
    new_status = get_status()

    if not new_status:
        failures += 1
        if failures >= 3:
            online = False
    else:
        failures = 0
        online = True

    if init_status != online:
        online = new_status
        print(f"Server status changed: Server is {'Online' if online else 'Offline'}")

    time.sleep(0.25)
