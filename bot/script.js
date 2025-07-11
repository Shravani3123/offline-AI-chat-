<!-- script.js -->
<script>
document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const voiceBtn = document.getElementById('voice-btn');
    const userInput = document.getElementById('user-input');
    const chatbox = document.getElementById('chatbox');
    const themeToggle = document.getElementById('theme-toggle');
    const newChatBtn = document.getElementById('new-chat-btn');
    const charCounter = document.getElementById('char-counter');
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const showSidebarBtn = document.getElementById('show-sidebar-btn');

    let currentChatId = Date.now().toString();

    // Update character counter
    userInput.addEventListener('input', () => {
        charCounter.textContent = ${userInput.value.length}/1000;
    });

    // Toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('hidden');
        sidebarToggle.textContent = sidebar.classList.contains('hidden') ? '☰' : '✕';
        showSidebarBtn.classList.toggle('hidden', !sidebar.classList.contains('hidden'));
    }

    sidebarToggle.addEventListener('click', toggleSidebar);
    showSidebarBtn.addEventListener('click', toggleSidebar);

    // Reset chat
    function resetChat() {
        currentChatId = Date.now().toString();
        chatbox.innerHTML = '<li class="chat incoming"><p>Welcome to the Chatbot! Type a message (max 1000 chars) or click the mic to start.</p></li>';
        charCounter.textContent = '0/1000';
        userInput.value = '';
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    // Start a new chat
    newChatBtn.addEventListener('click', resetChat);

    // Send message
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Simulate voice input
    voiceBtn.addEventListener('click', () => {
        const simulatedVoiceText = "Hello, this is a voice message!";
        displayMessage('outgoing', simulatedVoiceText);
        const botResponse = getBotResponse(simulatedVoiceText);
        setTimeout(() => displayMessage('incoming', botResponse), 500);
    });

    // Theme toggle
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        themeToggle.textContent = document.body.classList.contains('dark-mode') 
            ? '☀ Light Mode' 
            : '🌙 Dark Mode';
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            displayMessage('outgoing', message);
            userInput.value = '';
            charCounter.textContent = '0/1000';
            const botResponse = getBotResponse(message);
            setTimeout(() => displayMessage('incoming', botResponse), 500);
        }
    }

    function displayMessage(type, message) {
        const li = document.createElement('li');
        li.classList.add('chat', type);
        li.innerHTML = <p>${message}</p>;
        chatbox.appendChild(li);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function getBotResponse(message) {
        // Placeholder for backend logic
        return Echo: ${message}; // Replace with actual bot response
    }

    // Initialize with a new chat
    resetChat();
});
</script>
