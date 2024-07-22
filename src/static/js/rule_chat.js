document.addEventListener("DOMContentLoaded", function() {
    const messagesContainer = document.getElementById('messages');

    // 자동 스크롤을 위한 함수
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // 페이지 로드 시 자동으로 스크롤
    scrollToBottom();
});

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messages = document.getElementById('messages');

    function sendMessage() {
        const messageText = messageInput.value.trim();

        if (messageText === '') {
            return; // 입력이 비어있으면 아무 작업도 하지 않음
        }

        // 새로운 사용자 메시지 생성
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.innerHTML = `<div class="message-content">${messageText}</div>`;

        // 메시지를 messages 영역에 추가
        messages.appendChild(userMessage);

        // 입력 필드 비우기
        messageInput.value = '';

        // 메시지 영역 스크롤을 맨 아래로 이동
        messages.scrollTop = messages.scrollHeight;
    }

    // 전송 버튼 클릭 시 메시지 전송
    sendButton.addEventListener('click', () => {
        sendMessage();
    });

    // Enter 키를 눌렀을 때 메시지 전송
    messageInput.addEventListener('input', (event) => {
        // 임시로 처리 - Enter 키를 눌렀는지 확인
        if (event.data === '\n') {
            event.preventDefault(); // 기본 Enter 키 동작(줄바꿈) 방지
            sendMessage();
        }
    });

    // Enter 키를 눌렀을 때 메시지 전송
    messageInput.addEventListener('keydown', (event) => {
        if(event.isComposing) return; // 한글 2번 입력 버그 해소
        if (event.key === 'Enter') {
            event.preventDefault(); // 기본 Enter 키 동작(줄바꿈) 방지
            sendMessage();
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const messagesContainer = document.getElementById('messages');

    // 자동 스크롤을 위한 함수
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // 페이지 로드 시 자동으로 스크롤
    scrollToBottom();
});

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messages = document.getElementById('messages');

    function sendMessage() {
        const messageText = messageInput.value.trim();

        if (messageText === '') {
            return; // 입력이 비어있으면 아무 작업도 하지 않음
        }

        // 새로운 사용자 메시지 생성
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.innerHTML = `<div class="message-content">${messageText}</div>`;

        // 메시지를 messages 영역에 추가
        messages.appendChild(userMessage);

        // 입력 필드 비우기
        messageInput.value = '';

        // 메시지 영역 스크롤을 맨 아래로 이동
        messages.scrollTop = messages.scrollHeight;
    }

    // 전송 버튼 클릭 시 메시지 전송
    sendButton.addEventListener('click', () => {
        sendMessage();
    });

    // Enter 키를 눌렀을 때 메시지 전송
    messageInput.addEventListener('input', (event) => {
        // 임시로 처리 - Enter 키를 눌렀는지 확인
        if (event.data === '\n') {
            event.preventDefault(); // 기본 Enter 키 동작(줄바꿈) 방지
            sendMessage();
        }
    });

    // Enter 키를 눌렀을 때 메시지 전송
    messageInput.addEventListener('keydown', (event) => {
        if(event.isComposing) return; // 한글 2번 입력 버그 해소
        if (event.key === 'Enter') {
            event.preventDefault(); // 기본 Enter 키 동작(줄바꿈) 방지
            sendMessage();
        }
    });
});

