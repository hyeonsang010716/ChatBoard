document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messages = document.getElementById('messages');
    const fileAttach = document.getElementById('fileAttach');
    const messagesContainer = document.getElementById('messages');
    let messageText = messageInput.value.trim();

    // 자동 스크롤을 위한 함수
    function scrollToBottom() {
        messages.scrollTop = messages.scrollHeight;
    }

    function makeLoading() {
        const htmlString = '<div id="loading" class="message partner"><h2>답변을 생성 중입니다</h2><div class="circle"></div><div class="circle"></div><div class="circle"></div></div>';
        messagesContainer.innerHTML += htmlString;
        scrollToBottom();
    }

    function removeLoading() {
        const loading = document.getElementById("loading");
        loading.remove()
    }

    function makeResponseChat(response) {
        const htmlString = '<div class="message partner"><img src="https://i.ibb.co/W0wQy5Z/icon.png" alt="ICON"><div class="message-content">' + response + '</div></div>';
        messagesContainer.innerHTML += htmlString;
        scrollToBottom();
    }

    function sendQuestionQuery(query) {
        const game_text = document.querySelector('.description');
        const game_description = game_text.textContent || game_text.innerText;
        game_name = game_description.split('\n').map(line => line.trim()).filter(line => line !== '')
        console.log(game_name[0]);
        const data = {
            message : query ,
            name : game_name[0]
        }
        const queryString = new URLSearchParams(data).toString();        
        fetch('/chatboard/chatting?' + queryString) 
        .then(response => {
            if (!response) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text(); 
            })
            .then(data => {
                console.log(data)
                removeLoading();
                makeResponseChat(data);
                
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                
                // 에러 메시지 처리
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message partner';
                errorMessage.innerHTML = `<div class="message-content">Error: ${error.message}</div>`;
                messages.appendChild(errorMessage);
                removeLoading();
                makeResponseChat("오류가 발생했습니다. 다시 입력해주세요");
            })
            .finally(() => {
                // 입력 필드 활성화
                messageInput.readOnly = false;
                scrollToBottom(); // 새로운 메시지 추가 후 스크롤 이동
            });
    }

    function sendMessage() {
        messageText = messageInput.value.trim();
        messageInput.value = '';
        if (messageText === '') {
            return; // 입력이 비어있으면 아무 작업도 하지 않음
        }
        messageInput.readOnly = true;
        // 새로운 사용자 메시지 생성
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.innerHTML = `<div class="message-content">${messageText}</div>`;

        // 메시지를 messages 영역에 추가
        messages.appendChild(userMessage);

        // 메시지 영역 스크롤을 맨 아래로 이동
        scrollToBottom();

        // 여기서 쿼리 보내기
        makeLoading();
        sendQuestionQuery(messageText);

    };

    function sendImageMessage(file) {
        messageInput.readOnly = true;
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        // 파일 객체를 URL로 변환
        const fileURL = URL.createObjectURL(file);
        userMessage.innerHTML = `<div class="message-content"><img src="${fileURL}" alt="Image" style="max-width: 100%; height: auto;"></div>`;
        messages.appendChild(userMessage);
        makeLoading();
        sendQuestionQuery(); //이거를 바꾸긴해야 하는데
    }

    fileAttach.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            sendImageMessage(file)
        }
    });

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

    scrollToBottom(); // 새로운 콘텐츠 로드시 스크롤 최하단으로 보내기
});