document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');

    const logoButton = document.getElementById('logoButton');
    const searchForm = document.getElementById('search_form');
    const searchInput = document.getElementById('search_input');
    const contents = document.getElementById('contents');

    // 모든 보드게임 정보를 가져와서 화면에 표시하는 함수
    // async function loadBoardGames() {
    //     try {
    //         console.log('Fetching board games...');
    //         const gameListResponse = await fetch('/get_all_boardgames'); // 해당 부분의 링크는 이 파일에서 요청을 받아, 모든 보드게임 정보가 담긴 json을 반환해야 합니다.
    //         if (!gameListResponse.ok) {
    //             throw new Error('Network response was not ok ' + gameListResponse.statusText);
    //         }
    //         const data = await gameListResponse.json();
    //         console.log('Board games data:', data);
    //         displayBoardGames(data);
    //     } catch (error) {
    //         console.error('There was a problem with the fetch operation:', error);
    //     }
    // }

    // 모든 보드게임 정보를 가져와서 화면에 표시하는 함수, 여기서는 잠깐 임의로 json을 만들어서 사용중입니다.
    function loadBoardGames() {
        const boardGames = [
            {
                "image": "https://example.com/images/game1.jpg",
                "name": "Chess",
                "updated": "2024-07-22"
            },
            {
                "image": "https://example.com/images/game2.jpg",
                "name": "Monopoly",
                "updated": "2024-07-18"
            },
            {
                "image": "https://example.com/images/game3.jpg",
                "name": "Scrabble",
                "updated": "2024-07-20"
            },
            {
                "image": "https://example.com/images/game4.jpg",
                "name": "Settlers of Catan",
                "updated": "2024-07-15"
            }
        ];
        displayBoardGames(boardGames);
    }

    // 보드게임 데이터를 화면에 표시 및, 클릭하면 해당 클릭한 보드게임을 서버에 전달한 뒤 세부 게임 창으로 연결하는 함수
    function displayBoardGames(boardGames) {
        contents.innerHTML = ''; // 기존 콘텐츠를 제거
        boardGames.forEach(game => {
            const gameCard = document.createElement('div');
            gameCard.className = 'boardgame-card';
            gameCard.innerHTML = `
                <img src="${game.image}" alt="${game.name}">
                <div class="title">${game.name}</div>
                <div class="detail">${game.updated}</div>
            `;
            gameCard.addEventListener('click', () => {
                try {
                    // 해당 링크는 화면에서 보드게임을 선택하면 게임의 이름을 POST로 전달하고, 요청이 수락되면 룰 상세 설명 링크를 여는 기능을 해야 합니다.
                    // const pageResponse = fetch('/select_game', {
                    //     method: 'POST',
                    //     headers: {
                    //         'Content-Type': 'application/json'
                    //     },
                    //     body: JSON.stringify({ name: game.name })
                    // });
                    // if (!pageResponse.ok) {
                    //     throw new Error('Network response was not ok ' + pageResponse.statusText);
                    // }
                    // const data = pageResponse.json();
                    console.log('Game selected:', game.name);
                    // 성공적으로 전송 후, 특정 페이지로 이동
                    window.location.href = '/chatboard/sub-page';
                } catch (error) {
                    console.error('There was a problem with the fetch operation:', error);
                }
            });
            contents.appendChild(gameCard);
        });
    }

    // 페이지가 로드될 때 보드게임 정보를 가져옴
    loadBoardGames();

    // 로고 버튼을 클릭할 때 보드게임 정보를 다시 가져옴
    if (logoButton) {
        logoButton.addEventListener('click', (event) => {
            event.preventDefault();
            console.log('Logo button clicked, loading board games...');
            loadBoardGames();
        });
    } else {
        console.log('Logo button not found');
    }

    // 검색 폼 제출 처리
    searchForm.addEventListener('submit', async function(event) {
        event.preventDefault(); // 기본 폼 제출 동작을 막음
        console.log('Submit event fired');

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
