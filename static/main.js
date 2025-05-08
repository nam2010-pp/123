const socket = io();
const chatForm = document.getElementById('chat-form');
const chatBox = document.getElementById('chat-box');

// Lấy username từ phần tử HTML ẩn
const username = document.getElementById("username").innerText.trim();

// Lắng nghe sự kiện gửi tin nhắn
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = document.getElementById('message').value;

    // Gửi tin nhắn với cả username
    socket.emit('send_message', { username: username, message: message });
    document.getElementById('message').value = '';
});

// Lắng nghe sự kiện nhận tin nhắn
socket.on('receive_message', (data) => {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.innerHTML = `<strong>${data.username}</strong> (${data.timestamp}): ${data.message}`;
    chatBox.appendChild(messageDiv);

    // Tự động cuộn xuống cuối chat box
    chatBox.scrollTop = chatBox.scrollHeight;
});

// Dark mode toggle
const toggleBtn = document.getElementById("toggle-mode");
const body = document.body;

// Kiểm tra và load theme từ localStorage
if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
}

toggleBtn.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    localStorage.setItem("theme", body.classList.contains("dark-mode") ? "dark" : "light");
});
