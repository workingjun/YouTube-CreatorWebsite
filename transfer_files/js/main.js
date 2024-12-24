import './modules/menu.js';
import './modules/menu_click.js';
import './modules/sorting.js';
import './modules/play.js';
import './modules/comments.js';
import './modules/loading.js';
import './data/link.js';
import { sortVideos, filterVideos } from './modules/sorting.js';

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