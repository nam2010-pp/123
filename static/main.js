const socket = io();
const chatForm = document.getElementById('chat-form');
const chatBox = document.getElementById('chat-box');
const username = document.getElementById("username").innerText.trim();

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = document.getElementById('message').value;

    socket.emit('send_message', { username: username, message: message });
    document.getElementById('message').value = '';
});

socket.on('receive_message', (data) => {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'new');
    messageDiv.innerHTML = `<strong>${data.username}</strong> (${data.timestamp}): ${data.message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
});
