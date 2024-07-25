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

function hasScrollBehavior() {
    return 'scrollBehavior' in document.documentElement.style;
}
  
document.addEventListener("DOMContentLoaded", function () {
    document.removeEventListener("DOMContentLoaded", arguments.callee, false);
  
    window.addEventListener("scroll", toggleScrollUpButton);
  
    var e = document.getElementById('scroll-to-top');
    e.addEventListener('click', scrollToTop, false);
    }, false);