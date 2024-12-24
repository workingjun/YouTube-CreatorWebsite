import pandas as pd
from googleapiclient.discovery import build
import re, os
from dotenv import load_dotenv
from scripts.DataBase import DatabaseManager
from datetime import datetime

class YouTubeManager:
    def __init__(self, api_key, count=-1, channelID=None, channel_name=None):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.channel_name = channel_name
        if channelID is not None:
            self.channelID = channelID
        else:
            self.channelID = self.get_channel_id_by_name()
        self.count = count

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
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                order="relevance"
            )
            response = request.execute()

            # 댓글 정리
            comments_data = []
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                text = comment['textDisplay']  # 댓글 텍스트
                like_count = comment['likeCount']  # 좋아요 수
                author = comment['authorDisplayName']  # 작성자 이름
                text_clean = re.sub(r'<.*?>', '', text)  # HTML 태그 제거
                comments_data.append({"author":author,"text":text_clean,"like_count":like_count})  # 작성자 추가
            return comments_data
        except:
            return None
        
    def statistics(self, video_id): 
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        for item in response['items']:
            if 'viewCount' not in item['statistics']:
                return None
            video_id = item.get('id', 'Unknown ID')
            duration = item.get("contentDetails", {}).get("duration", "")
            is_short = 0
            match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
            if match:
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2) or 0)
                seconds = int(match.group(3) or 0)
                total_seconds = hours * 3600 + minutes * 60 + seconds
                if total_seconds <= 60:
                    is_short = 1
            # print(f"Is Shorts = {is_short}, Duration = {duration}, total_seconds={total_seconds}")  
            publish_time = item['snippet']['publishedAt'].replace("T", " ").replace("Z", "")
            publish_time_list=list(publish_time)
            previous_time = ''.join(publish_time_list[11:13])
            plus_time = int(previous_time) + 9
            publish_time_list[11:13] = str(plus_time)
            publish_time = "".join(publish_time_list)  
            publish_time = datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")    
            return {
                'video_id': video_id,
                'title': item['snippet']['localized']['title'],
                'view_count': int(item['statistics']['viewCount']),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'publish_time': publish_time,
                'is_shorts': is_short
            }
    
    def collect_data(self, db_manager: DatabaseManager):
        videos_data = []
        comments_data = {}
        try:
            db_manager.cursor.execute("SELECT video_id FROM videoId")
            video_ids = [row[0] for row in db_manager.cursor.fetchall()]
        except Exception as e:
            print(f"[Error] Failed to fetch video IDs from database: {e}")
            return
        for video_id in video_ids[:self.count]:
            stats = self.statistics(video_id)
            if stats is None:
                continue
            videos_data.append(stats)
            db_manager.upsert_videodata(
                video_id=stats['video_id'],
                title=stats['title'],
                view_count=stats['view_count'],
                like_count=stats['like_count'],
                comment_count=stats['comment_count'],
                publish_time=stats['publish_time'],
                is_shorts=stats['is_shorts']
            )
            data = self.textDisplay(video_id)
            if data is None:
                continue
            comments_data[f"{video_id}"] = data
            for comment in data:
                db_manager.upsert_comments(
                    video_id=video_id,
                    author=comment['author'],
                    text=comment['text'],
                    like_count=comment['like_count']
                )
        return video_ids[:self.count]

    def save_videoId(self, page, db_manager: DatabaseManager):
        next_page_token = None
        video_ids = []
        for _ in range(page):
            request = self.youtube.search().list(
                part="snippet",
                channelId=self.channelID,
                maxResults=50,
                order="date",
                pageToken=next_page_token
            )
            response = request.execute()
            for item in response['items']:
                if item['id']['kind'] == "youtube#video":
                    video_ids.append(item['id']['videoId'])
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        for video_id in video_ids[:self.count]:
            db_manager.upsert_videoId(video_id)
            
    def get_all_playlists(self):
        next_page_token = None
        playlists = []
        while True:
            request = self.youtube.playlists().list(
                part="snippet",
                channelId=self.channelID,
                maxResults=10,  # 한 번에 최대 50개
                pageToken=next_page_token
            )
            response = request.execute()
            # 재생목록 정보를 리스트에 추가
            for item in response['items']:
                playlists.append(item["id"])
            # 다음 페이지 토큰
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        return playlists

    def save_videoId_from_playlist(self, db_manager: DatabaseManager):
        playlist_ids = self.get_all_playlists()  # 업로드 재생목록 ID 가져오기
        next_page_token = None
        video_ids = []
        for playlist_id in playlist_ids:
            while True:
                request = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()
                for item in response['items']:
                    video_ids.append(item['snippet']['resourceId']['videoId'])
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
        for video_id in video_ids[:self.count]:
            db_manager.upsert_videoId(video_id)

if __name__=="__main__":
    load_dotenv("secrets/.env.google")
    api_key = os.getenv("api_key1")
    youtube_manager = YouTubeManager(
        api_key=api_key, 
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        count=-1
        )
    #youtube_manager.save_videoId()
    youtube_manager.collect_data()





