document.addEventListener('DOMContentLoaded', () => {
    const logoButton = document.getElementById('logoButton');
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    const contents = document.getElementById('contents');

    // 모든 보드게임 정보를 가져와서 화면에 표시하는 함수
    async function loadBoardGames() {
        try {
            const response = await fetch('/get_all_boardgames'); // 이 URL은 서버 엔드포인트로 변경해야 합니다.
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const data = await response.json();
            displayBoardGames(data);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    // 보드게임 데이터를 화면에 표시하는 함수
    function displayBoardGames(boardGames) {
        contents.innerHTML = ''; // 기존 콘텐츠를 제거
        boardGames.forEach(game => {
            const gameCard = document.createElement('div');
            gameCard.className = 'boardgame-card';
            gameCard.innerHTML = `
                <img src="${game.image}" alt="${game.title}">
                <div class="title">${game.title}</div>
                <div class="updated">Updated ${game.updated}</div>
            `;
            contents.appendChild(gameCard);
        });
    }

    // 페이지가 로드될 때 보드게임 정보를 가져옴
    loadBoardGames();

    // 로고 버튼을 클릭할 때 보드게임 정보를 다시 가져옴
    logoButton.addEventListener('click', (event) => {
        event.preventDefault();
        loadBoardGames();
    });

    // 검색 폼 제출 처리
    searchForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // 기본 폼 제출 동작을 막음

        const searchText = searchInput.value;
        console.log('Search Text:', searchText);

        try {
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: searchText })
            });
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            const data = await response.json();
            console.log('Search Response:', data);
            displayBoardGames(data);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    });
});
