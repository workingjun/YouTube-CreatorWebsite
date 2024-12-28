// 채널 정보 로드 및 렌더링
async function loadChannelInfo() {
    try {
        const channelInfoUrl = '/ChannelInfo';

        const response = await fetch(channelInfoUrl);
        if (!response.ok) throw new Error('채널 정보 API 요청 실패');

        const channelInfo = await response.json();

        // DOM 요소에 데이터 삽입
        document.getElementById('channel-link').href = `https://www.youtube.com/channel/${channelInfo.channelID}`;
        document.getElementById('channel-thumbnail').src = channelInfo.thumbnail;
        document.getElementById('channel-name').textContent = channelInfo.title;
        document.getElementById('subscriber-count').textContent = channelInfo.subscriber_count.toLocaleString();
        document.getElementById('channel-description').textContent = channelInfo.description;
        document.getElementById('views-count').textContent = channelInfo.views_count.toLocaleString();
        document.getElementById('video-count').textContent = channelInfo.video_count.toLocaleString();
    } catch (error) {
        console.error('채널 정보 로드 실패:', error);
    }
}

// 링크 데이터 로드 및 렌더링
async function loadLinks() {
    try {
        const linksUrl = '/LinkData';
        const response = await fetch(linksUrl);
        if (!response.ok) throw new Error('링크 API 요청 실패');

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
        console.error('링크 데이터 로드 실패:', error);
    }
}

// DOM 로드 완료 시 데이터 로드
document.addEventListener('DOMContentLoaded', () => {
    loadChannelInfo();
    loadLinks();
});
