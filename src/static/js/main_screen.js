document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');

    let allBoardGames = []

    const logoButton = document.getElementById('logoButton');
    const searchForm = document.getElementById('search_form');
    const searchInput = document.getElementById('search_input');
    const contents = document.getElementById('contents');

    // 모든 보드게임 정보를 가져와서 화면에 표시하는 함수
    async function loadBoardGames() {
        try {
            console.log('Fetching board games...');
            const gameListResponse = await fetchGameJson(); // 해당 부분은 이 파일에서 요청을 받아, 모든 보드게임 정보가 담긴 json을 반환해야 합니다.
            console.log('Fetch Complete!')
            const data = await gameListResponse.json();
            console.log('Board games data:', data);

            allBoardGames = data.games;
            console.log(allBoardGames);
            displayBoardGames(data.games);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    // 보드게임 데이터를 화면에 표시 및, 클릭하면 해당 클릭한 보드게임을 서버에 전달한 뒤 세부 게임 창으로 연결하는 함수
    function displayBoardGames(boardGames) {
        const contents = document.getElementById('contents');
        contents.innerHTML = ''; // 기존 콘텐츠를 제거
        boardGames.forEach(game => {
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
                    console.log('Game selected:', game.name);
                    // 성공적으로 전송 후, 특정 페이지로 이동
                    postGameJson(game);
                } catch (error) {
                    console.error('There was a problem with the fetch operation:', error);
                }
            });
            contents.appendChild(gameCard);
        });
    }

    // 페이지가 로드될 때 보드게임 정보를 가져옴
    loadBoardGames();

    // 검색 폼 제출 처리
    searchForm.addEventListener('submit', function(event) {
        event.preventDefault(); // 기본 폼 제출 동작을 막음
        console.log('Submit event fired');

        const searchText = searchInput.value.toLowerCase();
        console.log('Search Text:', searchText);

        const filteredGames = allBoardGames.filter(game => game.name.toLowerCase().includes(searchText));
        console.log('Filtered Games:', filteredGames);
        displayBoardGames(filteredGames);
    });

/* 검색 버튼을 누르면 해당 기준에 맞는 보드게임 등을 뽑아내고, 화면에 보여주는 함수 */
    document.getElementById('elementSearch').addEventListener('click', () => {
        const selectedCriteria = {
            players: getSelectedButtonText(document.getElementById('players')),
            theme: getSelectedButtonText(document.getElementById('theme')),
            difficulty: getSelectedButtonText(document.getElementById('difficulty'))
        };

        const results = searchGames(selectedCriteria);
        console.log(results);
        displayBoardGames(results);
    });

    function getSelectedButtonText(category) {
        const activeButton = category.querySelector('button.active');
        return activeButton ? activeButton.textContent : null;
    }

    function searchGames(criteria) {
        return allBoardGames.filter(game => {
            const [minPlayers, maxPlayers] = game.players.split('-').map(Number);
            const playerCount = criteria.players ? Number(criteria.players.replace('인', '')) : null;

            const matchesPlayers = !criteria.players || (playerCount >= minPlayers && playerCount <= maxPlayers);
            const matchesTheme = !criteria.theme || game.theme.includes(criteria.theme);
            const matchesDifficulty = !criteria.difficulty || game.difficulty === criteria.difficulty;

            return matchesPlayers && matchesTheme && matchesDifficulty;
        });
    }
});

async function fetchGameJson() {
    try {
        const response = await fetch('/chatboard/game_json');
        return response;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

function postGameJson(data) {
    const queryString = new URLSearchParams(data).toString();
    window.location.href = '/chatboard/sub-page?' + queryString;
}

function hasScrollBehavior() {
    return 'scrollBehavior' in document.documentElement.style;
}

/* 선택 기준 누르면 활성화되고, 다른 기준은 비활성화되는 기능을 하는 함수*/
document.querySelectorAll('.category').forEach(category => {
    category.addEventListener('click', (event) => {
        if (event.target.tagName === 'BUTTON') {
            const buttons = category.querySelectorAll('button');
            buttons.forEach(button => button.classList.remove('active'));
            event.target.classList.add('active');
        }
    });
});


/* Top 버튼 누르면 맨 위 화면으로 올라가는 기능을 하는 함수 */ 
function smoothScroll() {
    var currentY = window.scrollY;
    var int = setInterval(function () {
        window.scrollTo(0, currentY);
  
        if (currentY > 500) {
            currentY -= 70;
        } else if (currentY > 100) {
            currentY -= 50;
        } else {
            currentY -= 10;
        }
  
        if (currentY <= 0) clearInterval(int);
    }, 1000 / 60); // 60fps
}
  
function scrollToTop() {
    // document.getElementById('page-title').scrollIntoView({behavior: 'smooth'});
    if (hasScrollBehavior()) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        smoothScroll();
    }
}
  
function toggleScrollUpButton() {
    var y = window.scrollY;
    var e = document.getElementById('scroll-to-top');
    if (y >= 350) {
        e.style.transform = 'translateY(-30%)'
        e.style.opacity = 1;
    } else {
        e.style.opacity = 0;
        e.style.transform = 'translateY(30%)'
    }
}
  
document.addEventListener("DOMContentLoaded", function () {
    document.removeEventListener("DOMContentLoaded", arguments.callee, false);
  
    window.addEventListener("scroll", toggleScrollUpButton);
  
    var e = document.getElementById('scroll-to-top');
    e.addEventListener('click', scrollToTop, false);
    }, false);