const itemsPerLoad = 5;
let originalOrder = []; // 원래 DOM 순서 저장

export function initializeOriginalOrder() {
    const container = document.getElementById('popular-videos-container');
    originalOrder = Array.from(container.querySelectorAll('.video-card')); // 초기 DOM 순서 저장
}

export function sortVideos(criteria) {
    const container = document.getElementById('popular-videos-container');
    let videos = Array.from(container.querySelectorAll('.video-card'));

    // 필터링 적용
    if (criteria === 'Only Shorts') {
        videos = videos.filter(card => card.getAttribute('data-is-shorts') === '1'); // Shorts만 포함
    } else if (criteria === '기본') {
        videos = originalOrder; // 원래 순서 복원
    } else {
        // 정렬 기준 적용
        videos.sort((a, b) => {
            // 다른 기준 정렬
            const valueA = Number(a.getAttribute(`data-${criteria}`));
            const valueB = Number(b.getAttribute(`data-${criteria}`));
            return valueB - valueA; // 내림차순
        });
    }

    // 정렬된 요소를 다시 추가
    videos.forEach((video, index) => {
        container.appendChild(video);

        // hidden 클래스 처리
        if (index < itemsPerLoad) {
            if (video.classList.contains('hidden')) {
                video.classList.remove('hidden'); // 보여줄 비디오에서 hidden 제거
            }
        } else {
            if (!video.classList.contains('hidden')) {
                video.classList.add('hidden'); // 초과한 비디오에 hidden 추가
            }
        }
    });
}

// 전역 스코프에 추가
window.sortVideos = sortVideos;
