// JSON 파일 경로
const jsonFilePath = './js/data/link_data.json';

// JSON 파일 가져오기 및 렌더링
async function loadLinks() {
    try {
        const response = await fetch(jsonFilePath);

        if (!response.ok) throw new Error('JSON 파일을 불러오는 데 실패했습니다.');

        const linkData = await response.json();
        const linkList = document.getElementById('link-list');

        // JSON 데이터를 반복 처리
        Object.entries(linkData).forEach(([title, { image_link, external_link }]) => {
            // 링크 아이템 생성
            const linkItem = document.createElement('a');
            linkItem.className = 'link-item';
            linkItem.href = external_link;
            linkItem.target = '_blank';
            linkItem.rel = 'nofollow noopener noreferrer'; // 보안 강화

            // 이미지 태그 생성
            const img = document.createElement('img');
            img.src = image_link;
            img.alt = `${title} 아이콘`;
            img.loading = 'lazy'; // 이미지 지연 로드로 성능 최적화

            // 텍스트 컨테이너 생성
            const textContainer = document.createElement('span');
            textContainer.textContent = title;

            // 링크 아이템 구성
            linkItem.appendChild(img);
            linkItem.appendChild(textContainer);
            linkList.appendChild(linkItem);
        });
    } catch (error) {
        console.error('데이터 로드 실패:', error);
    }
}

// DOM 로드 완료 시 함수 호출
document.addEventListener('DOMContentLoaded', loadLinks);