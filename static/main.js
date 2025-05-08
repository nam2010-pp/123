const socket = io();
const chatForm = document.getElementById('chat-form');
const chatBox = document.getElementById('chat-box');
const username = document.getElementById("username").innerText.trim();

chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();
    if (!message) return;
    
    socket.emit('send_message', { username, message });
    messageInput.value = '';
});

socket.on('receive_message', (data) => {
    const messageDiv = document.createElement('div');
    messageDiv.className = "bg-indigo-100 p-2 rounded-md shadow-sm";
    messageDiv.innerHTML = `
        <p class="text-sm">
            <strong>${data.username}</strong> 
            <span class="text-xs text-gray-500">(${data.timestamp})</span>
        </p>
        <p>${data.message}</p>
    `;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
});
