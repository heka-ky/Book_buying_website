let isVoiceEnabled = true;  // 默认启用语音播报

// 语音播报
function speak(text) {
    if (!isVoiceEnabled) return; // 如果语音播报被禁用，直接返回
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'zh-CN';
        speechSynthesis.speak(utterance);
    }
}

document.getElementById('sendButton').addEventListener('click', () => {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text) return;

    addMessage('user', text);
    speak(text); // 播报用户消息
    input.value = '';

    // 发送请求到 Flask 后端
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
        const aiReply = data.reply || '[错误响应]';
        addMessage('ai', aiReply);
        speak(aiReply); // 播报 AI 回复
        saveConversation(text, aiReply); // 保存对话
    })
    .catch(err => {
        addMessage('ai', '[网络错误]');
        speak('[网络错误]'); // 播报网络错误
    });
});

// 处理用户输入的消息
function addMessage(role, content) {
    const container = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = `<div class="avatar">${role === 'ai' ? '🤖' : '🧑'}</div><div class="text">${content}</div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// 切换语音播报功能
document.getElementById('voiceToggle').addEventListener('click', () => {
    isVoiceEnabled = !isVoiceEnabled;
    const voiceToggleButton = document.getElementById('voiceToggle');

    if (isVoiceEnabled) {
        voiceToggleButton.classList.add('active');
        voiceToggleButton.innerText = '关闭语音播报';
    } else {
        voiceToggleButton.classList.remove('active');
        voiceToggleButton.innerText = '开启语音播报';

        // 关键：立即停止当前语音
        speechSynthesis.cancel();
    }
});

// 新建对话按钮功能
document.getElementById('newChat').addEventListener('click', () => {
    document.getElementById('messages').innerHTML = ''; // 清空当前消息
    addMessage('ai', '你好，我是你的AI助手。让我们开始对话吧！'); // 添加欢迎消息
    loadHistory(); // 加载历史对话
});

// 清空对话按钮功能
document.getElementById('clearChat').addEventListener('click', () => {
    document.getElementById('messages').innerHTML = ''; // 清空所有对话
    localStorage.removeItem('conversations'); // 清除存储的历史对话
    loadHistory(); // 更新下拉框
});

// 选择历史对话
document.getElementById('historySelect').addEventListener('change', (event) => {
    const selectedHistory = event.target.value;
    if (selectedHistory) {
        loadConversation(selectedHistory); // 加载选择的历史对话
    }
});

// 保存对话到 localStorage
function saveConversation(userMessage, aiReply) {
    const conversations = JSON.parse(localStorage.getItem('conversations')) || [];
    const newConversation = {
        userMessage,
        aiReply
    };
    conversations.push(newConversation);
    localStorage.setItem('conversations', JSON.stringify(conversations));
    loadHistory(); // 更新下拉框
}

// 加载所有历史对话的选择项
function loadHistory() {
    const historySelect = document.getElementById('historySelect');
    const conversations = JSON.parse(localStorage.getItem('conversations')) || [];
    historySelect.innerHTML = '<option value="">选择历史对话</option>'; // 重置下拉框内容
    conversations.forEach((conv, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `对话 ${index + 1}`;
        historySelect.appendChild(option);
    });
}

// 加载特定历史对话
function loadConversation(index) {
    const conversations = JSON.parse(localStorage.getItem('conversations')) || [];
    const conversation = conversations[index];
    if (conversation) {
        document.getElementById('messages').innerHTML = ''; // 清空当前对话
        addMessage('user', conversation.userMessage); // 显示用户消息
        addMessage('ai', conversation.aiReply); // 显示 AI 回复
    }
}

// 初始化：当页面加载时，添加默认的欢迎消息和加载历史对话
document.addEventListener('DOMContentLoaded', () => {
    addMessage('ai', '你好，我是你的AI助手。让我们开始对话吧！');
    loadHistory(); // 加载历史对话列表
});
