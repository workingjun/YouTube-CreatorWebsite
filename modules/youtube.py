import pandas as pd
from googleapiclient.discovery import build
import re, json, os
from dotenv import load_dotenv

class YouTubeManager:

    PATH1 = "youtube_data/videoId.json"
    PATH2 = "youtube_data/total_data.json"
    
    def __init__(self, api_key, count=-1, channelID=None, channel_name=None):
        # YouTube API 설정
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
            return {
                'title': video_title, 
                'video_id': video_id, 
                'comments': comments,
                'like_count': like_counts
                }
        except:
            return None
        
    def statistics(self, video_id): 
        request = self.youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        for item in response['items']:
            if 'viewCount' not in item['statistics']:
                return None
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
        with open(self.PATH1, "r", encoding="utf-8") as f:
            video_ids = json.load(f)
        for video_id in video_ids[:self.count]:
            stats = self.statistics(video_id)
            if stats is None:
                continue
            videos_data.append(stats)
            print(stats)
            data = self.textDisplay(video_id)
            if data is None:
                continue
            comments_data.append(data)
        if self.count != -1:
            with open(self.PATH2, "r", encoding="utf-8") as f:
                total_data = json.load(f)
                videos_data = videos_data + total_data["video"][self.count:]
                comments_data = comments_data + total_data["comments"][self.count:]
                total_data = {"video" : videos_data, "comments" : comments_data}
                with open(self.PATH2, "w", encoding="utf-8") as f:
                    json.dump(total_data, f, ensure_ascii=False, indent=4)
                    print("data json 파일 업데이트 완료")
        else:
            total_data = {"video" : videos_data, "comments" : comments_data}
            with open(self.PATH2, "w", encoding="utf-8") as f:
                json.dump(total_data, f, ensure_ascii=False, indent=4)
                print(f"total data json 파일 저장 완료")
        df_videos = pd.DataFrame(videos_data)
        df_comments = pd.DataFrame(comments_data)
        return df_videos, df_comments

    def save_videoId(self):
        next_page_token = None
        video_ids = []
        for _ in range(8):
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
        # JSON 파일로 저장
        with open(self.PATH1, "w", encoding="utf-8") as f:
            json.dump(video_ids, f, ensure_ascii=False, indent=4)
            print(f"{len(video_ids)}개 data json 파일 저장 완료")

if __name__=="__main__":
    load_dotenv("data/.env.google")
    api_key = os.getenv("api_key_update")
    youtube_manager = YouTubeManager(
        api_key=api_key, 
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        count=20
        )
    #youtube_manager.save_videoId()
    youtube_manager.collect_data()





