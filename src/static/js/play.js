document.addEventListener('DOMContentLoaded', () => {
    const videoCards = document.querySelectorAll('.video-card, .video-card-info');

    videoCards.forEach(card => {
        const thumbnail = card.querySelector('.thumbnail');
        const iframe = card.querySelector('iframe');
        const playButton = card.querySelector('.play-button');
        const videoId = card.dataset.videoId;

        // 비디오 시작 함수
        const startVideo = () => {
            if (!videoId || !iframe) return;

            // 썸네일과 버튼 숨김
            if (thumbnail) thumbnail.style.display = 'none';
            if (playButton) playButton.style.display = 'none';

            // iframe URL 설정
            if (!iframe.src.includes(videoId)) {
                iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&enablejsapi=1`;
            }

            // iframe 표시
            iframe.style.display = 'block';

            // "playing" 클래스를 추가하여 크기 확대
            card.classList.add('playing');
        };

        // 클릭 이벤트 설정
        if (thumbnail) thumbnail.addEventListener('click', startVideo);
        if (playButton) playButton.addEventListener('click', startVideo);

        // 확대된 상태에서 닫기
        card.addEventListener('click', (e) => {
            if (e.target === card && card.classList.contains('playing')) {
                // iframe 숨기기 및 리셋
                iframe.src = '';
                iframe.style.display = 'none';

                // 썸네일과 버튼 다시 표시
                if (thumbnail) thumbnail.style.display = 'block';
                if (playButton) playButton.style.display = 'block';

                // "playing" 클래스 제거
                card.classList.remove('playing');
            }
        });
    });
});