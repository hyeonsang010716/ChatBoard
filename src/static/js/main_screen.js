let allBoardGames = []
const domElement = {};

const noGamesMessages = [
    '저희는 그런 것 받지 않습니다... <br> 그렇지만, 이건 꼭 있었으면 하는 게임은 해당 링크로 문의해주세요!',
    '원래는 그런 게 있었는데, 잠깐 한눈 판 사이에 도망갔나봐요! <br> 해당 링크로, 찾으시는 보드게임을 보내주시겠어요?',
    '앗! 지금은 기준에 맞는 보드게임이 없어요! <br> 해당 링크로, 찾으시는 보드게임을 보내주시겠어요?',
    '이상하네요, 기준에 맞는 보드게임이 감쪽같이 사라졌어요! <br> 원하시는 게임을 링크로 알려주세요!',
    '해당 기준에 맞는 보드게임을 가져오는 데에 실패했습니다. <br> 원하시는 게임을 링크로 보내주세요.',
    '저도 아직 그 보드게임 모르는데! <br> 혹시 이 링크로, 저한테도 알려주실 수 있어요?',
    '보드게임이 없다고요? 걱정 마세요! <br> 이 링크로, 그 보드게임에 대해 보내주세요!',
    '저도 가끔 실수해요. 없을 때도 있는거죠 뭐, <br> 실망하지 마시고, 이 링크로 그 게임에 대해 보내주세요.'
];

/* DOM content가 load 되면 불러와지는 부분,
이 부분이 사실상 main 이라고 생각하면 된다 */
document.addEventListener('DOMContentLoaded', () => {
    domElement.searchForm = document.getElementById('search_form');
    domElement.searchInput = document.getElementById('search_input');
    domElement.element = document.getElementById('element');
    domElement.contents = document.getElementById('contents');
    domElement.toggleButton = document.getElementById('toggleSearch');
    domElement.elementSearch = document.getElementById('elementSearch');

    // 페이지가 로드될 때 보드게임 정보를 가져옴
    loadBoardGames();

    // 각종 이벤트 리스너 호출
    setupEventListeners();
});

// 모든 보드게임 정보를 가져와서 화면에 표시하는 함수
async function loadBoardGames() {
    try {
        const gameListResponse = await fetchGameJson(); // 해당 부분은 이 파일에서 요청을 받아, 모든 보드게임 정보가 담긴 json을 반환해야 함.
        const data = await gameListResponse.json();

        allBoardGames = data.games;
        displayBoardGames(data.games);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

// game_json에서 게임 정보들에 대한 json을 가져오는 함수
async function fetchGameJson() {
    try {
        const response = await fetch('/chatboard/game_json');
        return response;
    } catch (error) {
        throw error;
    }
}

// 보드게임 카드를 화면에 표시하는 함수
function displayBoardGames(boardGames) {
    domElement.contents.innerHTML = ''; // 기존 콘텐츠를 제거
    if (boardGames.length === 0) {
        domElement.contents.style.display = 'flex';
        const randomIndex = Math.floor(Math.random() * noGamesMessages.length);
        const randomMessage = noGamesMessages[randomIndex];

        const noGamesMessage = document.createElement('div');
        noGamesMessage.className = 'noGamesAlert';
        noGamesMessage.innerHTML = `
            <img src= "https://i.ibb.co/W0wQy5Z/icon.png">
            <p> ${randomMessage} </p>
            <a href="https://forms.gle/QyQZzdySyMpiFdrZ8" id="email">문의사항 링크</a>
        `;
        domElement.contents.appendChild(noGamesMessage);
    } else {
        boardGames.forEach(game => {
            domElement.contents.style.display = 'grid';
            const gameCard = createGameCard(game);
            domElement.contents.appendChild(gameCard);
        });
    }
}

// 보드게임 카드를 생성하고 세부룰로 연결하는 기능을 구현한 함수
function createGameCard(game) {
    const gameCard = document.createElement('div');
    gameCard.className = 'boardgame-card';
    gameCard.innerHTML = `
        <img src="${game.image}" alt="${game.name}">
        <div class="title">${game.name}</div>
        <div class="detail">${game.players}인 | ${game.difficulty} | ${game.playtime} | ${game.theme} </div>
    `;
    /* 해당 부분은, 각 보드게임마다 클릭하면 클릭한 보드게임을 전달하고 rule_chat 화면으로 전달하는 기능이 구현됨 */
    gameCard.addEventListener('click', () => {
        try {
            postGameJson(game.name);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    });
    return gameCard;
}

// data를 받아, 해당 data와 연결되는 주소로 이동하는 함수
function postGameJson(data) {
    const Data = {
        name: data
    };
    const queryString = new URLSearchParams(Data).toString();
    window.location.href = '/chatboard/sub-page?' + queryString;
}

/* 이벤트 리스너들을 추가하는 함수.
이 함수는 DOM이 로드될 때 실행될 것임 */
function setupEventListeners() {
    domElement.toggleButton.addEventListener('click', toggleSearch);
    domElement.searchForm.addEventListener('submit', nameSearchSubmit);
    domElement.elementSearch.addEventListener('click', elementSearchSubmit);
    document.querySelectorAll('.category').forEach(category => {
        category.addEventListener('click', handleCategoryClick);
    });
}

// 검색 기준 바꾸는 버튼에 대한 함수
function toggleSearch() {
    if (domElement.searchForm.style.display === 'none') {
        domElement.searchForm.style.display = 'flex';
        domElement.element.style.display = 'none';
        domElement.toggleButton.innerText = ' ▼ 유형으로 검색하기 ';
    } else {
        domElement.searchForm.style.display = 'none';
        domElement.element.style.display = 'flex';
        domElement.toggleButton.innerText = ' ▲ 이름으로 검색하기 ';
    }
}

// 이름으로 검색하는 폼 제출 처리하는 함수
function nameSearchSubmit(event) {
    event.preventDefault();

    // 입력된 검색어에서 모든 공백 제거
    const searchText = domElement.searchInput.value.toLowerCase().trim().replace(/\s+/g, '');

    const filteredGames = allBoardGames.filter(game => {
        // 보드게임 이름에서도 모든 공백 제거
        const gameName = game.name.toLowerCase().trim().replace(/\s+/g, '');
        return gameName.includes(searchText);
    });
    displayBoardGames(filteredGames);
}

/* 선택 기준 누르면 활성화되고, 다른 기준은 비활성화되는 기능을 하는 함수 
   이미 선택한 기준을 클릭하는 경우, 해당 기준이 비활성화되기도 함. */
function handleCategoryClick(event) {
    if (event.target.tagName === 'BUTTON') {
        const buttons = event.currentTarget.querySelectorAll('button');
        const targetButton = event.target;

        if (targetButton.classList.contains('active')) {
            targetButton.classList.remove('active');
        } else {
            buttons.forEach(button => button.classList.remove('active'));
            event.target.classList.add('active');
        }
    }
}

// 선택된 검색 기준을 전달하고 화면에 보여주는 함수
function elementSearchSubmit() {
    const selectedCriteria = {
        players: getSelectedButtonText(document.getElementById('players')),
        theme: getSelectedButtonText(document.getElementById('theme')),
        difficulty: getSelectedButtonText(document.getElementById('difficulty'))
    };

    const results = searchGames(selectedCriteria);
    displayBoardGames(results);
}

/* 선택한 기준의 텍스트를 전달하는 함수.
   선택한 기준이 없다면 null을 전달한다. 이 처리는 다른 함수에서 진행. */
   function getSelectedButtonText(category) {
    const activeButton = category.querySelector('button.active');
    return activeButton ? activeButton.textContent : null;
}

// 해당 기준에 맞는 보드게임들을 반환하는 함수
function searchGames(criteria) {
    return allBoardGames.filter(game => {
        const [minPlayers, maxPlayers] = game.players.split('-').map(Number);
        const playerCount = criteria.players && criteria.players !== "6인 이상" ? Number(criteria.players.replace('인', '')) : null;

        const matchesPlayers = !criteria.players || 
                    (criteria.players === "6인 이상" && maxPlayers >= 6) || 
                    (playerCount >= minPlayers && playerCount <= maxPlayers);
        const matchesTheme = !criteria.theme || game.theme.includes(criteria.theme);
        const matchesDifficulty = !criteria.difficulty || game.difficulty === criteria.difficulty;

        return matchesPlayers && matchesTheme && matchesDifficulty;
    });
}