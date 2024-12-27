import './components/menu.js';
import './utils/sorting.js';
import './components/play.js';
import './components/comments.js';
import './utils/loading.js';
import './data/link.js';
import { sortVideos } from './utils/sorting.js';

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