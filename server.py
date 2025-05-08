# render_app.py
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

VPS_API = "http://147.185.221.28:24404"  # hoặc link playit.gg

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

        # Gửi user lên VPS
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        try:
            res = requests.post(f"{VPS_API}/save_user", json={
                "username": username,
                "password": hashed
            })
            if res.json().get("status") == "exists":
                return "Tài khoản đã tồn tại!"
        except:
            return "Lỗi khi kết nối VPS!"

        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    try:
        res = requests.get(f"{VPS_API}/users")
        users = res.json()
    except:
        users = []

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

    # Gửi lên VPS
    try:
        requests.post(f"{VPS_API}/save", json={
            "username": username,
            "message": message
        })
    except Exception as e:
        print("Lỗi gửi về VPS:", e)

    # Phát lại cho các client
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
