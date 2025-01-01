document.addEventListener('DOMContentLoaded', function () {
    const videoCards = document.querySelectorAll('.video-card, .video-card-info');

    videoCards.forEach(card => {
        const titleLink = card.querySelector('h3 a');
        
        titleLink.addEventListener('click', async function (event) {
            event.preventDefault(); // 기본 동작 방지

            // videoId 추출
            const videoId = card.getAttribute('data-video-id');
            const group = card.getAttribute('data-group'); // 'friendshiping' 또는 'suhyeon'
            
            // 로딩 스피너 표시
            const loadingSpinner = document.getElementById('loading-spinner');
            loadingSpinner.style.display = 'flex';

            try {
                // 댓글 데이터 가져오기 (Flask API 호출)
                const response = await fetch(`/${group}/comments?videoId=${videoId}`);
                const comments = await response.json();

                // 댓글 모달 생성
                showCommentsModal(videoId, comments);
            } catch (error) {
                console.error('댓글 데이터를 가져오는 중 오류가 발생했습니다.', error);
            } finally {
                // 로딩 스피너 숨기기
                loadingSpinner.style.display = 'none';
            }
        });
    });
    
    // 댓글 모달 생성 함수
    function showCommentsModal(videoId, comments) {
        let modal = document.getElementById('comments-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'comments-modal';
            modal.style.position = 'fixed';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
            modal.style.zIndex = '1000';
            modal.style.display = 'flex';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            document.body.appendChild(modal);
        }

        modal.innerHTML = `
            <div style="position: relative; background: white; padding: 20px; border-radius: 10px; max-width: 600px; max-height: 80%; overflow-y: auto;">
                <button id="close-modal-btn" style="position: absolute; top: 10px; right: 10px; background: transparent; border: none; font-size: 20px; cursor: pointer;" onclick="closeCommentsModal()">×</button>
                ${comments.length === 0 ? '<p>댓글이 없습니다.</p>' : `
                    <ul>
                        ${comments.map(comment => `
                            <li style="margin-bottom: 15px; border-bottom: 1px solid #ddd; padding-bottom: 10px;">
                                <p><strong>${comment.author}</strong></p>
                                <p>${comment.text}</p>
                                <p>좋아요 수: ${comment.like_count}</p>
                            </li>`).join('')}
                    </ul>
                `}
                <button id="close-modal-btn" style="margin-top: 20px; padding: 10px 20px; background: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer;" onclick="closeCommentsModal()">닫기</button>
            </div>
        `;

        modal.style.display = 'flex'; // 모달 표시
    }
});

// 모듈 방식으로 내보내기
export function closeCommentsModal() {
    const modal = document.getElementById('comments-modal');
    if (modal) modal.style.display = 'none';
}

// 전역 스코프에 추가
window.closeCommentsModal = closeCommentsModal;