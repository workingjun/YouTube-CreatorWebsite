import pandas as pd
from googleapiclient.discovery import build
import re, json, os

class YouTubeManager:
    def __init__(self, api_key, channelID=None, channel_name=None):
        # YouTube API 설정
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.channel_name = channel_name
        if channelID is not None:
            self.channelID = channelID
        else:
            self.channelID = self.get_channel_id_by_name()

    def get_channel_id_by_name(self):
        """채널 이름으로 채널 ID를 가져오는 함수"""
        request = self.youtube.search().list(
            part='snippet',
            q=self.channel_name,  # 검색어 (채널 이름)
            type='channel',  # 채널만 검색
            maxResults=1     # 검색 결과 개수
        )
        response = request.execute()
        
        if response['items']:
            # 검색 결과에서 채널 ID와 이름 추출
            channel_info = response['items'][0]
            channel_id = channel_info['id']['channelId']
            return channel_id
        else:
            return None
        
    def ChannelInformation(self):
        request = self.youtube.channels().list(
            part="snippet,statistics",
            id=self.channelID
        )
        response = request.execute()
        channel_info = response['items'][0]
        result = {
            'title': channel_info['snippet']['title'],  # 채널 이름
            'channelID' : self.channelID,
            'description': channel_info['snippet']['description'],  # 채널 설명
            'thumbnail': channel_info['snippet']['thumbnails']['high']['url'],  # 채널 프로필 이미지
            'subscriber_count': int(channel_info['statistics']['subscriberCount']),  # 구독자 수
            'video_count': channel_info['statistics']['videoCount'],  # 동영상 수
            'views_count': channel_info['statistics']['viewCount']  # 전체 조회수
        }
        return result

    def textDisplay(self, video_id):
        # 동영상 정보 요청
        video_request = self.youtube.videos().list(
            part="snippet",
            id=video_id  # 영상 ID
        )
        video_response = video_request.execute()

        # 영상 제목 추출
        video_title = video_response['items'][0]['snippet']['title']

        request = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="relevance"
        )
        response = request.execute()

        # 댓글 정리
        comments = []
        like_counts = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            text = comment['textDisplay']
            like_count = comment['likeCount']
            text_clean = re.sub(r'<.*?>', '', text)
            comments.append(text_clean)
            like_counts.append(like_count)
        return video_title, comments, like_counts

    def statistics(self, video_id): 
        request = self.youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        for item in response['items']:
            return {
                'video_id': video_id,
                'title': item['snippet']['localized']['title'],
                'view_count': int(item['statistics']['viewCount']),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'publish_time': item['snippet']['publishedAt']
            }

    def collect_data(self):
        videos_data = []
        comments_data = []

        if os.path.exists("data/videoId.json"):
            # JSON 파일 읽기
            with open("data/videoId.json", "r", encoding="utf-8") as f:
                video_ids = json.load(f)
        else:
            self.save_videoId()
            # JSON 파일 읽기
            with open("data/videoId.json", "r", encoding="utf-8") as f:
                video_ids = json.load(f)

        for video_id in video_ids:
            stats = self.statistics(video_id)
            videos_data.append(stats)

            video_title, comments, like_counts = self.textDisplay(video_id)
            comments_data.append({
                'title': video_title, 
                'video_id': video_id, 
                'comments': comments,
                'like_count': like_counts
                })
        df_videos = pd.DataFrame(videos_data)
        df_comments = pd.DataFrame(comments_data)

        return df_videos, df_comments
    
    def save_videoId(self, count=100):
        request = self.youtube.search().list(
            part="snippet",
            channelId=self.channelID,
            maxResults=count,
            order="date"
        )
        video_ids = []
        response = request.execute()
        for item in response['items']:
            if item['id']['kind'] == "youtube#video":
                video_ids.append(item['id']['videoId'])

        # JSON 파일로 저장
        with open("data/videoId.json", "w", encoding="utf-8") as f:
            json.dump(video_ids, f, ensure_ascii=False, indent=4)
            print("json 파일 저장 완료")




