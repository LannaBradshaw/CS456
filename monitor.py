import os, subprocess, sys, time, requests

AUTH_SERVICE_PATH = os.path.join(os.path.dirname(__file__), "auth.py")
STANDBY_PATH = os.path.join(os.path.dirname(__file__), "standby.activate")

try:
    os.remove(STANDBY_PATH)
except OSError:
    pass

subprocess.Popen([sys.executable, AUTH_SERVICE_PATH])
subprocess.Popen([sys.executable, AUTH_SERVICE_PATH, "--standby"])

online = False
failures = 0
failover_started = False


def get_status():
    try:
        response = requests.get("http://localhost:5555/status")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        # print(f"Error occurred: {e}")
        return False


for _ in range(20):
    if get_status():
        online = True
        break
    time.sleep(0.25)

print(f"Initial status: Server is {'Online' if online else 'Offline'}")

while True:
    init_status = online
    new_status = get_status()

    if not new_status:
        failures += 1
        if failures >= 3:
            online = False

            if not failover_started:
                print(f"[Crash Detected]")
                try:
                    open(STANDBY_PATH, "a").close()
                    failover_started = True
                    print(f"[Failover Triggered]")
                except OSError:
                    print("Warm standby could not be activated")
    else:
        failures = 0
        online = True
        if failover_started:
            print(f"[Service Restored]")
            failover_started = False

    if init_status != online:
        online = new_status
        print(f"Server status changed: Server is {'Online' if online else 'Offline'}")

    time.sleep(0.25)
