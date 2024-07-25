function openDetailFrame(){
    detail.style.display = "block";
}

function closeDetailAnimation() {
    detail.querySelector('.detail-content').style.animation = 'slideOut 0.5s';
    detail.style.animation = 'fadeOut 0.5s';
    setTimeout(() => {
        detail.style.display = "none";
        detail.querySelector('.detail-content').style.animation = 'slideIn 0.5s';
        detail.style.animation = 'fadeIn 0.5s';
    }, 500);
}

document.addEventListener("DOMContentLoaded", () => {
    window.addEventListener("click", (event) => {
        if (event.target == detail) {
            closeDetailAnimation();
        }
    });

});
