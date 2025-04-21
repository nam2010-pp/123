const socket = io();
const chatForm = document.getElementById('chat-form');
const chatBox = document.getElementById('chat-box');

// Lấy username từ phần tử HTML ẩn
const username = document.getElementById("username").innerText.trim();

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = document.getElementById('message').value;

    // Gửi tin nhắn với cả username
    socket.emit('send_message', { username: username, message: message });
    document.getElementById('message').value = '';
});

socket.on('receive_message', (data) => {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.innerHTML = `<strong>${data.username}</strong> (${data.timestamp}): ${data.message}`;
    chatBox.appendChild(messageDiv);

    // Tự động cuộn xuống cuối chat box
    chatBox.scrollTop = chatBox.scrollHeight;
});
