document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messages = document.getElementById('messages');
    const fileAttach = document.getElementById('fileAttach');
    const messagesContainer = document.getElementById('messages');

    // 자동 스크롤을 위한 함수
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function makeLoading() {
        const htmlString = '<div id="loading" class="message partner"><h2>답변을 생성 중입니다</h2><div class="circle"></div><div class="circle"></div><div class="circle"></div></div>';
        messagesContainer.innerHTML += htmlString;
    }

    function removeLoading() {
        const loading = document.getElementById("loading");
        loading.remove()
    }

    function sendQuestionQuery() {
        // 쿼리는 string으로 전달하고 string 으로 결과값을 받아온다.
        fetch('http://127.0.0.1:5000/get-data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('result').innerText = JSON.stringify(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
           
    }

    function sendMessage() {
        const messageText = messageInput.value.trim();
        messageInput.readOnly = false;
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

        // 입력 필드 비우기
        messageInput.value = '';

        // 메시지 영역 스크롤을 맨 아래로 이동
        messages.scrollTop = messages.scrollHeight;

        // 여기서 쿼리 보내기
        makeLoading();
        sendQuestionQuery();
        //

    };

    fileAttach.addEventListener('click', () => {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
    
        if (!file) {
            alert('Please select a file!');
            return;
        }
    
        const formData = new FormData();
        formData.append('file', file);
    
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/upload', true);
    
        xhr.upload.onprogress = function(event) {
            if (event.lengthComputable) {
                const percentComplete = (event.loaded / event.total) * 100;
                document.getElementById('progress').innerText = `Upload progress: ${percentComplete.toFixed(2)}%`;
            }
        };
    
        xhr.onload = function() {
            if (xhr.status === 200) {
                alert('File uploaded successfully!');
            } else {
                alert('File upload failed!');
            }
        };
    
        xhr.send(formData);
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