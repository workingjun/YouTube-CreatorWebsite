// 모든 섹션과 메뉴 항목 가져오기
const sections = document.querySelectorAll('#channel-info, #recent-videos, #popular-videos-container');
const navLinks = document.querySelectorAll('.menu ul li a');

// 스크롤 위치에 따라 활성화 업데이트
function updateActiveLink() {
    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 50; // 메뉴 높이 고려
        const sectionHeight = section.clientHeight;

        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        const hrefValue = link.getAttribute('href').substring(1);
        if (hrefValue === currentSection) {
            link.classList.add('active');
        }
    });
}

// 스크롤 이벤트 등록
window.addEventListener('scroll', updateActiveLink);

// 클릭 이벤트 등록
navLinks.forEach(menuItem => {
    menuItem.addEventListener('click', function (e) {
        e.preventDefault();

        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);

        if (targetSection) {
            window.scrollTo({
                top: targetSection.offsetTop - 50, // 메뉴 높이 고려
                behavior: 'smooth',
            });
        }

        // 클릭된 메뉴 항목에 'active' 클래스 추가
        navLinks.forEach(link => link.classList.remove('active'));
        this.classList.add('active');
    });
});

document.querySelectorAll('.menu a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);
        targetElement.scrollIntoView({ behavior: 'smooth' });
    });
});