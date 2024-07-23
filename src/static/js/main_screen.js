// 검색창 부분 전달.
document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search_form');
    const searchInput = document.getElementById('search_input');

    searchForm.addEventListener('submit', () => {
        event.preventDefault();

        const searchText = searchInput.value;
        console.log(searchText)

        // 서버에 해당 검색어 요청 보내고 response로 받아오는 기능.
        fetch('/server', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({query:searchText})
        })
        .then(
            response => response.json()
        )
        .then(data => {
            console.log("response: ", data);
        })
        .catch(error => {
            console.log("Error: ", error)
        });
    });
});