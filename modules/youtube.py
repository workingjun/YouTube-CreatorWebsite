import pandas as pd
from googleapiclient.discovery import build
import re 

class YouTubeManager:
    def __init__(self, channelId):
        # YouTube API 설정
        api_key = "AIzaSyDA38IZdJjA6BEgkUe_TKeQc2q9YPUf0xE"
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.channelId = channelId

    def ChannelInformation(self):
        request = self.youtube.channels().list(
            part="snippet,statistics",
            id=self.channelId
        )
        response = request.execute()
        channelName = response['items'][0]['snippet']['title']
        subscriberCount = int(response['items'][0]['statistics']['subscriberCount'])
        information = [channelName, self.channelId, subscriberCount]
        return information

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
            maxResults=50,
            order="relevance"
        )
        response = request.execute()

        # 댓글 정리
        comments = []
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comment_clean = re.sub(r'<.*?>', '', comment)
            comments.append(comment_clean)
        return video_title, comments

    def videoId(self, count):
        request = self.youtube.search().list(
            part="snippet",
            channelId=self.channelId,
            maxResults=count,
            order="date"
        )
        video_ids = []
        response = request.execute()
        for item in response['items']:
            if item['id']['kind'] == "youtube#video":
                video_ids.append(item['id']['videoId'])
        return video_ids

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

        for video_id in self.videoId(20):
            stats = self.statistics(video_id)
            videos_data.append(stats)

            video_title, comments = self.textDisplay(video_id)
            comments_data.append({
                'title': video_title, 
                'video_id': video_id, 
                'comments': comments
                })
        df_videos = pd.DataFrame(videos_data)
        df_comments = pd.DataFrame(comments_data)

        return df_videos, df_comments



