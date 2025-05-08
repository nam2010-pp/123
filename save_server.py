# server_vps.py
from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
MESSAGES_FILE = "messages.json"
USERS_FILE = "users.json"

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        return json.load(f)

@app.route("/save", methods=["POST"])
def save_message():
    data = request.get_json()
    messages = load_json(MESSAGES_FILE)
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append(data)
    save_json(MESSAGES_FILE, messages)
    return {"status": "ok"}

@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(load_json(MESSAGES_FILE))

@app.route("/save_user", methods=["POST"])
def save_user():
    user = request.get_json()
    users = load_json(USERS_FILE)
    if any(u["username"] == user["username"] for u in users):
        return {"status": "exists"}
    users.append(user)
    save_json(USERS_FILE, users)
    return {"status": "saved"}

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(load_json(USERS_FILE))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
