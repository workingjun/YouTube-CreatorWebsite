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
            video_ids = [row["video_id"] for row in self.api_manager.get_videoIds()] 
        else:
            video_ids = [row["video_id"] for row in db_manager.fetch_videoIds()]
        if not update_video_ids:
            db_manager.upsert_videoIds(video_ids_list=video_ids)
        video_data = []
        for video_id in video_ids:
            stats = self.api_manager.get_video_statistics(video_id)
            if stats is None:
                continue
            video_data.append(stats)
        db_manager.upsert_videoData(video_data_list=video_data)
    
    def save_channel_information(self):
        results = self.api_manager.get_channel_information()
        with open(self.ChannelInfo_filepath, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)