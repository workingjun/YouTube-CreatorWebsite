import { getItemsPerLoad } from './loading.js';

let filteredVideoCards = []; // 필터링된 비디오 카드
let currentIndex = 0; // 현재 로드된 비디오 카드의 인덱스
const itemsPerLoad = getItemsPerLoad();

export function sortVideos(criteria) {
    const container = document.getElementById('popular-videos-container');
    const videos = Array.from(container.querySelectorAll('.video-card'));

    // 정렬
    const sortedVideos = videos.sort((a, b) => {
        if (criteria === 'date') {
            // 날짜 정렬: 내림차순
            const dateA = new Date(a.getAttribute('data-date')); // 'data-date' 속성에서 날짜 가져오기
            const dateB = new Date(b.getAttribute('data-date'));
            return dateB - dateA; // 최신 날짜가 먼저 오도록 정렬
        } else {
            // 다른 기준 정렬
            const valueA = Number(a.getAttribute(`data-${criteria}`));
            const valueB = Number(b.getAttribute(`data-${criteria}`));
            return valueB - valueA; // 내림차순
        }
    });

    // 정렬된 요소를 다시 추가
    sortedVideos.forEach((video, index) => {
        container.appendChild(video);

        // hidden 클래스 처리
        if (index < itemsPerLoad) {
            video.classList.remove('hidden'); // 보여줄 비디오에서 hidden 제거
        } else {
            video.classList.add('hidden'); // 초과한 비디오에 hidden 추가
        }
    });
}

export function filterVideos(criteria) {
    // 기준에 따라 비디오 카드 필터링
    const allVideoCards = document.querySelectorAll('.video-card');
    if (criteria === 'shorts') {
        // data-is-shorts="true" 속성이 있는 카드만 포함
        filteredVideoCards = Array.from(allVideoCards).filter(card =>
            card.getAttribute('data-is-shorts') === 'true' // 문자열로 비교
        );
    } else {
        // 다른 기준일 경우 모든 카드를 필터링 결과로 설정
        filteredVideoCards = Array.from(allVideoCards);
    }

    // 모든 카드를 숨기고 필터링된 카드만 표시
    allVideoCards.forEach(card => card.classList.add('hidden'));
    filteredVideoCards.forEach((card, index) => {
        if (index < itemsPerLoad) {
            card.classList.remove('hidden');
        }
    });

    // 필터 초기화
    currentIndex = Math.min(itemsPerLoad, filteredVideoCards.length); // 필터링된 후 보여줄 인덱스 관리
}

// 전역 스코프에 추가
window.filterVideos = filterVideos;
