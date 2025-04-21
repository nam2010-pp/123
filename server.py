from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
import json
import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

# Đường dẫn file JSON
USERS_FILE = "users.json"
MESSAGES_FILE = "messages.json"

# Đọc dữ liệu từ file JSON
def read_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

# Ghi dữ liệu vào file JSON
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
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users.append({"username": username, "password": hashed_password})
        write_json(USERS_FILE, users)
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    users = read_json(USERS_FILE)
    user = next((user for user in users if user["username"] == username), None)

    # Kiểm tra mật khẩu
    if user and bcrypt.check_password_hash(user["password"], password):
        session["username"] = username
        return redirect(url_for("chat"))
    return "Sai tên đăng nhập hoặc mật khẩu!"

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("home"))
    messages = read_json(MESSAGES_FILE)
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

    messages = read_json(MESSAGES_FILE)
    messages.append({"username": username, "message": message, "timestamp": timestamp})
    write_json(MESSAGES_FILE, messages)

    emit("receive_message", {"username": username, "message": message, "timestamp": timestamp}, broadcast=True)

# Route phục vụ ads.txt
@app.route("/ads.txt")
def ads_txt():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "ads.txt")
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Lấy cổng từ biến môi trường
    socketio.run(app, host="0.0.0.0", port=port)
