from DB.database import MySQLYouTubeDB
from config.api_config import api_key
from scripts.youtubeAPI.api_manager import YoutubeApiManager
import json

class YouTubeManager:
    def __init__(self, api_key, channelID=None, channel_name=None):
        self.ChannelInfo_filepath = "./json/ChannelInfo.json"
        self.api_manager = YoutubeApiManager(
            api_key=api_key, 
            channelID=channelID, 
            channel_name=channel_name
        )
    
    def collect_data(self, db_manager: MySQLYouTubeDB, update_video_ids:bool=False):
        if update_video_ids:
            video_ids_list = self.api_manager.get_videoIds() 
            db_manager.upsert_videoIds(video_ids_list=video_ids_list)
            video_ids = [row['video_id'] for row in video_ids_list]
        else:
            video_ids = db_manager.fetch_videoIds()
        video_data = []
        for video_id in video_ids:
            stats = self.api_manager.get_video_statistics(video_id)
            if stats is None:
                continue
            video_data.append(stats)
        batch_size = 100  # 한 번에 처리할 데이터 크기
        for i in range(0, len(video_data), batch_size):
            batch = video_data[i:i+batch_size]
            db_manager.upsert_videoData(video_data_list=batch)
    
    def save_channel_information(self):
        results = self.api_manager.get_channel_information()
        with open(self.ChannelInfo_filepath, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)