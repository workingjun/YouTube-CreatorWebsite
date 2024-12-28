let isLoading = false;
let currentIndex = 0; // 현재 로드된 비디오 카드의 인덱스
const itemsPerLoad = 5;

function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function loadMoreVideos() {
    if (isLoading) return;
    isLoading = true;
    showLoading();

    setTimeout(() => {
        const videoCards = document.querySelectorAll('.video-card.hidden');

        // 현재 숨겨진 카드 중에서 표시할 갯수만큼 로드
        for (let i = 0; i < itemsPerLoad && currentIndex < videoCards.length; i++, currentIndex++) {
            videoCards[currentIndex].classList.remove('hidden');
        }

        hideLoading();
        isLoading = false;

        // 모든 카드가 표시되면 로딩 중단
        if (currentIndex >= videoCards.length) {
            window.removeEventListener('scroll', handleScroll);
        }
    }, 500); // 0.5초 지연 (예제용)
}

function handleScroll() {
    // 스크롤이 페이지 하단에 도달했는지 확인
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
        loadMoreVideos();
    }
}

// 초기 로드 시 첫 데이터 표시
loadMoreVideos();
window.addEventListener('scroll', handleScroll);

// itemsPerLoad 값을 반환하는 함수
export function getItemsPerLoad() {
    return  itemsPerLoad;
}