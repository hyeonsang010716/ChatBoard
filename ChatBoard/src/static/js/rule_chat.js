document.addEventListener("DOMContentLoaded", function() {
    const messagesContainer = document.getElementById('messages');

    // 자동 스크롤을 위한 함수
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // 페이지 로드 시 자동으로 스크롤
    scrollToBottom();
});
