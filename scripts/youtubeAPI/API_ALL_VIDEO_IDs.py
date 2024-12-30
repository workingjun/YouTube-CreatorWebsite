def fetch_all_playlists(youtube, channel_id):
    """채널에서 모든 재생목록 ID를 가져오기"""
    playlist_ids = []
    next_page_token = None

    while True:
        # API 요청
        response = youtube.playlists().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        # 재생목록 ID 저장
        for item in response.get("items", []):
            playlist_ids.append(item["id"])

        # 다음 페이지로 이동
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # 더 이상 페이지가 없으면 종료

    return playlist_ids

def fetch_all_playlist_items(youtube, playlist_ids):
    """모든 재생목록에서 비디오 ID와 업로드 날짜를 가져오기"""
    all_video_data = []

    for playlist_id in playlist_ids:
        next_page_token = None

        while True:
            # playlistItems.list API 호출
            response = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            # 현재 페이지의 데이터를 처리
            for item in response.get("items", []):
                video_id = item["snippet"]["resourceId"]["videoId"]
                published_time = item["snippet"]["publishedAt"]
                all_video_data.append({
                    "video_id": video_id,
                    "published_time": published_time
                })

            # 다음 페이지로 이동
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break  # 더 이상 페이지가 없으면 종료
    return all_video_data

def fetch_shorts_videos(youtube, channel_id):
    """채널에서 모든 비디오 ID를 가져오기 (최소한의 요청으로, Shorts 포함)"""
    video_data = []
    next_page_token = None

    while True:
        # 비디오 검색 API 호출 (최대 50개, 페이지 토큰을 사용해 반복)
        response = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type="video"
        ).execute()

        # 비디오 ID 및 정보 저장
        for item in response.get("items", []):
            video_id = item["id"]["videoId"]
            published_time = item["snippet"]["publishedAt"]
            video_data.append({
                "video_id": video_id,
                "publish_time": published_time
            })

        # 다음 페이지로 이동
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # 더 이상 페이지가 없으면 종료

    return video_data


