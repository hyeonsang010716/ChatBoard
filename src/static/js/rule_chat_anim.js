document.addEventListener("DOMContentLoaded", () => {
    const detail = document.getElementById("detail");
    const openDetail = document.getElementById("openDetail");
    const closeDetail = document.getElementById("closeDetail");

    openDetail.addEventListener("click", () => {
        detail.style.display = "block";
    });

    closeDetail.addEventListener("click", () => {
        closeDetailAnimation();
    });

    window.addEventListener("click", (event) => {
        if (event.target == detail) {
            closeDetailAnimation();
        }
    });

    function closeDetailAnimation() {
        detail.querySelector('.detail-content').style.animation = 'slideOut 0.5s';
        detail.style.animation = 'fadeOut 0.5s';
        setTimeout(() => {
            detail.style.display = "none";
            detail.querySelector('.detail-content').style.animation = 'slideIn 0.5s';
            detail.style.animation = 'fadeIn 0.5s';
        }, 500);
    }
});
