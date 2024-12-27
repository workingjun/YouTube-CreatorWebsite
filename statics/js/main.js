import './menu.js';
import './sorting.js';
import './play.js';
import './comments.js';
import './loading.js';
import './channel_info.js';
import { sortVideos } from './sorting.js';

function handleSortChange() {
    const criteria = document.getElementById("sortCriteria").value;
    sortVideos(criteria);
}

// DOMContentLoaded 이벤트로 DOM이 로드된 후 이벤트 리스너 추가
document.addEventListener('DOMContentLoaded', () => {
    const sortCriteria = document.getElementById("sortCriteria");
    if (sortCriteria) {
        sortCriteria.addEventListener('change', handleSortChange);
    }
});