from googleapiclient.discovery import build
from scripts.youtubeAPI.response_handler import YouTubeResponseHandler 

class YoutubeApiManager:
    def __init__(self, api_key, channelID=None, channel_name=None):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.channel_name = channel_name
        self.channelID = channelID or self.get_channel_id_by_name()
    
    def fetch_response(self, api_name, **params):
        """API 요청과 응답 처리"""
        request = self.youtube.__getattribute__(api_name.split(".")[0])().list(**params)
        response = request.execute()

        return YouTubeResponseHandler.parse_response(api_name=api_name, response=response)
    
    def get_channel_information(self):
        return self.fetch_response(
            "channels.list",
            part="snippet,statistics",
            id=self.channelID
        )

    def get_video_statistics(self, video_id):
        return self.fetch_response(
            "videos.list",
            part="snippet,contentDetails,statistics",
            id=video_id
        )

    def get_comments(self, video_id):
        return self.fetch_response(
            "commentThreads.list",
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="relevance"
        )

    def get_videoIds(self):
        return self.fetch_response(
            "search.Idlist",
            part="snippet",
            channelId=self.channelID,
            maxResults=10,
            order="date",
        )
    
    def get_channel_id_by_name(self):
        return self.fetch_response(
            "search.list",
            part='snippet',
            q=self.channel_name,  # 검색어 (채널 이름)
            type='channel',  # 채널만 검색
            maxResults=1     # 검색 결과 개수
        )
    
    
    