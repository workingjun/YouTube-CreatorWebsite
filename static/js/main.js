import './menu.js';
import './sorting.js';
import './play.js';
import './comments.js';
import './loading.js';
import './channel_info.js';
import { sortVideos } from './sorting.js';
import { closeCommentsModal } from "./comments.js";

async function handleSortChange() {
    const criteria = document.getElementById("sortCriteria").value;
    sortVideos(criteria);
    
}

// DOMContentLoaded 이벤트로 DOM이 로드된 후 초기화
document.addEventListener('DOMContentLoaded', () => {
    try {
        // 정렬 기준 변경 이벤트 리스너 추가
        const sortCriteria = document.getElementById("sortCriteria");
        if (sortCriteria) {
            sortCriteria.addEventListener('change', handleSortChange);
        } else {
            console.warn("Sort criteria element not found during initialization.");
        }

        // 댓글 닫기 버튼 이벤트 리스너 추가
        const closeModalButton = document.getElementById("close-modal-btn");
        if (closeModalButton) {
            closeModalButton.addEventListener('click', closeCommentsModal);
        } else {
            console.warn("Close modal button not found.");
        }
    } catch (error) {
        console.error("Error during DOMContentLoaded initialization:", error);
    }
});