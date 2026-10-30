import json, os, random, secrets, sys, time

from flask import Flask, jsonify, request

app = Flask(__name__)
CHECKPOINT_PATH = os.path.join(os.path.dirname(__file__), "auth_checkpoint.json")
ACTIVATION_PATH = os.path.join(os.path.dirname(__file__), "standby.activate")


def load_sessions():
    try:
        with open(CHECKPOINT_PATH, "r", encoding="utf-8") as checkpoint:
            data = json.load(checkpoint)
        sessions = data.get("sessions", {})
        return sessions if isinstance(sessions, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def save_sessions():
    try:
        with open(CHECKPOINT_PATH, "w", encoding="utf-8") as checkpoint:
            json.dump({"sessions": sessions}, checkpoint)
    except OSError:
        pass


sessions = load_sessions()

CREDENTIALS = {"admin": "password123", "user": "password"}


@app.route("/login", methods=["POST"])
def authenticate():
    global sessions
    data = request.get_json() or {}

    fail = random.randint(1, 100)

    if fail < 5:
        os._exit(1)

    username = data.get("username")
    password = data.get("password")

    if username in CREDENTIALS and CREDENTIALS[username] == password:
        sessions = {
            token: owner for token, owner in sessions.items() if owner != username
        }
        token = secrets.token_hex(32)
        sessions[token] = username
        save_sessions()

        return jsonify(
            {"success": True, "message": "Authenticated successfully", "token": token}
        ), 200

    return jsonify({"success": False, "message": "Authentication unsuccessful"}), 401


@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Server is running"}), 200

@app.route("/session", methods=["GET"])
def session():
    token = request.args.get("token")
    if token not in sessions:
        return jsonify({"success": False, "message": "Invalid session token"}), 401
    return jsonify({"success": True, "username": sessions[token]}), 200


def run_standby():
    global sessions

    while not os.path.exists(ACTIVATION_PATH):
        time.sleep(0.1)

    try:
        os.remove(ACTIVATION_PATH)
    except OSError:
        pass

    sessions = load_sessions()
    app.run(host="0.0.0.0", port=5555, debug=False)


if __name__ == "__main__":
    if "--standby" in sys.argv:
        run_standby()
    else:
        app.run(host="0.0.0.0", port=5555, debug=False)
