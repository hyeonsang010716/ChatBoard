document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messages = document.getElementById('messages');
    const fileAttach = document.getElementById('fileAttach');
    const fileInput = document.getElementById('fileInput');
    const messagesContainer = document.getElementById('messages');
    const applyButton = document.getElementById('applyButton')
    let messageText = messageInput.value.trim();
    let formData = new FormData();
    let players = 0;


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

    function sendQuestionQueryWithImage() {
        fetch('/chatboard/img_upload', {
            method: 'POST',
            body: formData,
            players: players
          })
          .then(response => response.json())
          .then(data => {
            removeLoading();
            makeResponseChat(data["data"]);
          })
          .catch(error => {
            removeLoading();
            console.error('Error:', error);
          })
          .finally(() => {
            // 입력 필드 활성화
            formData = new FormData();
            messageInput.readOnly = false;
            scrollToBottom(); // 새로운 메시지 추가 후 스크롤 이동
        });
    }

    function sendQuestionQuery() {
        const data = {
            message: formData.get("message"),
            name: formData.get("name"),
            players: players
        };
        const queryString = new URLSearchParams(data).toString();
        fetch('/chatboard/chatting?' + queryString)
            .then(response => {
                if (!response.ok) { // 수정: response.ok로 확인
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.text();
            })
            .then(data => {
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
                formData = new FormData();
                messageInput.readOnly = false;
                scrollToBottom(); // 새로운 메시지 추가 후 스크롤 이동
            });
    }

    function sendQueryBranch() {
        const game_text = document.querySelector('.description');
        const game_description = game_text.textContent || game_text.innerText;
        const game_name = game_description.split('\n').map(line => line.trim()).filter(line => line !== ''); // 수정: const 추가
        formData.append("name", game_name[0]);

        

        if (formData.get("file") == null) sendQuestionQuery();
        else{
            sendQuestionQueryWithImage();
        } 
    } // 수정: 함수 닫는 괄호 추가

    function sendMessage() {
        // 메세지 전송
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
        formData.append("message", messageText);
        // 메시지 영역 스크롤을 맨 아래로 이동
        scrollToBottom();

        // 여기서 쿼리 보내기
        makeLoading();
        sendQueryBranch();
    }

    fileAttach.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (event) => {
        // 역할을 사진을 받으면 일단 출력 하는 용도로 사용
        const file = event.target.files[0];
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        const fileURL = URL.createObjectURL(file);
        formData.append('file', file);
        userMessage.innerHTML = `<div class="message-content"><img src="${fileURL}" alt="Image" style="max-width: 400px; height: auto;"></div>`;
        messages.appendChild(userMessage);
        
        const partnerMessage = document.createElement('div');
        partnerMessage.className = 'message partner';
        partnerMessage.innerHTML = `<img src="https://i.ibb.co/W0wQy5Z/icon.png" alt="ICON"><div class="message-content">현재 어떤 상황인가요? 사진에 대한 자세한 설명을 해주세요!</div>`;
        messages.appendChild(partnerMessage);
        scrollToBottom();

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
        if (event.isComposing) return; // 한글 2번 입력 버그 해소
        if (event.key === 'Enter') {
            event.preventDefault(); // 기본 Enter 키 동작(줄바꿈) 방지
            sendMessage();
        }
    });
    
    applyButton.addEventListener('click', () => {
        players = document.getElementById('howMany').value;
        document.getElementById('notification').style.display = 'none';
    });

    scrollToBottom(); // 새로운 콘텐츠 로드시 스크롤 최하단으로 보내기
});

document.addEventListener('DOMContentLoaded', () => {
    //console.log('DOMContentLoaded event fired');
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const Name = urlParams.get('name');
        const data = {
            name: Name
        };
        const queryString = new URLSearchParams(data).toString();
        fetch('/chatboard/game_detail?' + queryString)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(gameData => {
                const description = document.getElementById("scriptFrame");
                description.innerHTML = `
                <img src="${gameData["image"]}" alt="img" class="gameImg">
                <div class="description">
                    <h3>${gameData["name"]} </h3>
                    플레이어 인원 수: ${gameData["players"]} 
                    <br>
                    연령: ${gameData["age"]} 
                    <br>
                    난이도: ${gameData["difficulty"]} 
                    <br>
                    게임 진행 시간: ${gameData["playtime"]} 
                    <br>
                    <button id="openDetail" onclick="openDetailFrame()">게임 설명 보기</button>       
                </div>
                <div id="detail" class="detail">
                    <div class="detail-content">
                        <span id="closeDetail" onclick="closeDetailAnimation()">&times;</span>
                        <h2>게임 설명</h2>
                        <p>${gameData["description"]} </p>
                    </div>
                </div>
                    `
            })
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
});