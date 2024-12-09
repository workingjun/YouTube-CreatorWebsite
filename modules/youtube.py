import pandas as pd
from googleapiclient.discovery import build
import re, json, os
from dotenv import load_dotenv

class YouTubeManager:

    PATH1 = "youtube_data/videoId.json"
    PATH2 = "youtube_data/vidoes_data.json"
    PATH3 = "youtube_data/transfer_files/comments_data.json"
    
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
        comments_data = {}
        with open(self.PATH1, "r", encoding="utf-8") as f:
            video_ids = json.load(f)
        for video_id in video_ids[:self.count]:
            stats = self.statistics(video_id)
            if stats is None:
                continue
            videos_data.append(stats)
            #print(stats)
            data = self.textDisplay(video_id)
            if data is None:
                continue
            comments_data[f"{video_id}"] = data
        if self.count != -1:
             # PATH2 업데이트
            with open(self.PATH2, "r+", encoding="utf-8") as f:
                videos_data_prime = json.load(f)
                videos_data = videos_data + videos_data_prime[self.count:]
                f.seek(0)  # 파일 처음으로 이동
                json.dump(videos_data, f, ensure_ascii=False, indent=4)
                f.truncate()  # 파일 내용 자르기
                print("videos data json 파일 업데이트 완료 (PATH2)")

            # PATH3 업데이트
            with open(self.PATH3, "r+", encoding="utf-8") as f:
                comments_data_prime = json.load(f)
                comments_data_prime.update(comments_data)  # 기존 데이터와 병합
                f.seek(0)  # 파일 처음으로 이동
                json.dump(comments_data_prime, f, ensure_ascii=False, indent=4)
                f.truncate()  # 파일 내용 자르기
                print("comments data json 파일 업데이트 완료 (PATH3)")

        else:
            with open(self.PATH2, "w", encoding="utf-8") as f:
                json.dump(videos_data, f, ensure_ascii=False, indent=4)
                print(f"videos data json 파일 저장 완료")
            
            with open(self.PATH3, "w", encoding="utf-8") as f:
                json.dump(comments_data, f, ensure_ascii=False, indent=4)
                print(f"comments data json 파일 저장 완료")
        df_videos = pd.DataFrame(videos_data)
        return df_videos

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
    load_dotenv("youtube_data/.env.google")
    api_key = os.getenv("api_key_always")
    youtube_manager = YouTubeManager(
        api_key=api_key, 
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        count=-1
        )
    #youtube_manager.save_videoId()
    youtube_manager.collect_data()





