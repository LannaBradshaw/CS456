#adversarial audit script

import json, os, shutil, sys, time, requests

BASE_URL = "http://127.0.0.1:5555"
CHECKPOINT = "auth_checkpoint.json"
ACTIVATE = "standby.activate"


#check if the server is up
def is_up():
    try:
        return requests.get(BASE_URL + "/status", timeout=2).status_code == 200
    except requests.RequestException:
        return False


#wait for the standby to take over after a crash
def wait_for_server():
    for _ in range(60):
        if is_up():
            return True
        time.sleep(0.25)
    return False


#spam logins until the random crash fires and the primary dies
def crash_primary():
    for _ in range(200):
        try:
            requests.post(BASE_URL + "/login", json={"username": "?", "password": "?"}, timeout=1)
        except requests.RequestException:
            print("Primary crashed")
            return
        time.sleep(0.02)


#Scenario 1: induced false failover
def test_failover():
    print("Primary up before attack:", is_up())
    open(ACTIVATE, "a").close()
    print("Created standby.activate while the primary is still alive")
    time.sleep(3)
    print("Primary up after attack:", is_up())
    print("Check the standby terminal: did it start a second server on port 5555 (split-brain) or fail?")


#Scenario 2: tampered checkpoint
def test_checkpoint():
    requests.post(BASE_URL + "/login", json={"username": "admin", "password": "password123"})
    shutil.copy(CHECKPOINT, CHECKPOINT + ".bak")

    open(CHECKPOINT, "w").write("this is not valid json")
    print("Corrupted the checkpoint file")

    crash_primary()
    came_back = wait_for_server()
    print("Server recovered after loading the corrupted checkpoint:", came_back)

    shutil.move(CHECKPOINT + ".bak", CHECKPOINT)


#pick which test to run from the command line
if len(sys.argv) < 2:
    print("run: python audit.py failover or checkpoint")
elif sys.argv[1] == "failover":
    test_failover()
elif sys.argv[1] == "checkpoint":
    test_checkpoint()
else:
    print("unknown test:", sys.argv[1])