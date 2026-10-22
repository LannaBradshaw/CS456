from flask import Flask, request, jsonify
import os, secrets, random

app = Flask(__name__)
sessions = {}

CREDENTIALS = {"admin" : "password123", "user":"password"}

@app.route("/login", methods=["POST"])
def authenticate():
    data = request.get_json() or {}

    fail = random.randint(1, 100)

    if fail < 5:
        os._exit(1)

    username = data.get("username")
    password = data.get("password")

    if username in CREDENTIALS and CREDENTIALS[username] == password:
        token = secrets.token_hex(32)
        sessions[token] = username

        return jsonify({
            "success": True,
            "message": "Authenticated successfully",
            "token": token
        }), 200

    return jsonify({
        "success": False,
        "message": "Authentication unsuccessful"
    }), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=False)