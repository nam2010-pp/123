from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
MESSAGES_FILE = "messages.json"

def save_message(data):
    if not os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, "w") as f:
            json.dump([], f)
    with open(MESSAGES_FILE, "r") as f:
        messages = json.load(f)
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append(data)
    with open(MESSAGES_FILE, "w") as f:
        json.dump(messages, f, indent=4)

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    save_message(data)
    return {"status": "ok"}

@app.route("/messages", methods=["GET"])
def get_messages():
    if not os.path.exists(MESSAGES_FILE):
        return jsonify([])
    with open(MESSAGES_FILE, "r") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090)
