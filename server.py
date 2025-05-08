from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
import json
import datetime
import os
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

USERS_FILE = "users.json"
VPS_API = "http://147.185.221.28:24404"  # <-- Đổi <ip_vps> thành IP hoặc domain VPS thật

def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except:
        return []

def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = read_json(USERS_FILE)
        if any(user["username"] == username for user in users):
            return "Tên đăng nhập đã tồn tại!"
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        users.append({"username": username, "password": hashed})
        write_json(USERS_FILE, users)
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    users = read_json(USERS_FILE)
    user = next((u for u in users if u["username"] == username), None)
    if user and bcrypt.check_password_hash(user["password"], password):
        session["username"] = username
        return redirect(url_for("chat"))
    return "Sai tên đăng nhập hoặc mật khẩu!"

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("home"))
    try:
        res = requests.get(f"{VPS_API}/messages")
        messages = res.json()
    except:
        messages = []
    return render_template("chat.html", username=session["username"], messages=messages)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

@socketio.on("send_message")
def handle_message(data):
    username = data["username"]
    message = data["message"]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        requests.post(f"{VPS_API}/save", json={
            "username": username,
            "message": message
        })
    except Exception as e:
        print("Lỗi gửi về VPS:", e)

    emit("receive_message", {
        "username": username,
        "message": message,
        "timestamp": timestamp
    }, broadcast=True)

@app.route("/ads.txt")
def ads_txt():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "ads.txt")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
