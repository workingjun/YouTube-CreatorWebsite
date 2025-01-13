let isLoading = false;
let currentIndex = 0; // 현재 로드된 비디오 카드의 인덱스
const itemsPerLoad = 5;

function showLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) loadingElement.style.display = 'block';
}

function hideLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) loadingElement.style.display = 'none';
}

function loadMoreVideos() {
    if (isLoading) return;
    isLoading = true;
    showLoading();

    setTimeout(() => {
        const videoCards = document.querySelectorAll('.video-card'); // 전체 비디오 카드
        for (let i = 0; i < itemsPerLoad && currentIndex < videoCards.length; i++, currentIndex++) {
            if (videoCards[currentIndex].classList.contains('hidden')) {
                videoCards[currentIndex].classList.remove('hidden');
            }
        }

        hideLoading();
        isLoading = false;

        if (currentIndex >= videoCards.length) {
            window.removeEventListener('scroll', handleScroll);
        }
    }, 200);
}

// scroll 이벤트 최적화
function handleScroll() {
    // requestAnimationFrame을 사용하여 스크롤 이벤트 최적화
    if (!this.isScrolling) {
        this.isScrolling = true;
        requestAnimationFrame(() => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
                loadMoreVideos();
            }
            this.isScrolling = false;
        });
    }
}

// 초기 로드 시 첫 데이터 표시
loadMoreVideos();
window.addEventListener('scroll', handleScroll);

// itemsPerLoad 값을 반환하는 함수
export function getItemsPerLoad() {
    return itemsPerLoad;
}
