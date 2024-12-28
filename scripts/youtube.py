from DB.database import MySQLYouTubeDB
from scripts.youtubeAPI.api_manager import YoutubeApiManager
from scripts.utils.utils import DBManager
import json

class YouTubeManager:
    def __init__(self, db_manager: MySQLYouTubeDB, api_key, channelID=None, channel_name=None, finish_all_video_ids:bool=False):
        self.ChannelInfo_filepath = "./json/ChannelInfo.json"
        self.count = -1 if finish_all_video_ids else 5
        self.api_manager = YoutubeApiManager(
            api_key=api_key, 
            channelID=channelID, 
            channel_name=channel_name
        )
        self.db_manager = db_manager

    def return_video_ids(self, flags: bool):
        if flags:
            return [row["video_id"] for row in self.db_manager.fetch_videoIds()]
        return [row["video_id"] for row in self.api_manager.get_videoIds()] 
    
    def collect_data(self, flags):
        video_ids = self.return_video_ids(flags)
        for video_id in video_ids[:self.count]:
            stats = self.api_manager.get_video_statistics(video_id)
            if stats is None:
                continue
            self.db_manager.upsert_videoData(
                video_id=stats['video_id'],
                title=stats['title'],
                view_count=stats['view_count'],
                like_count=stats['like_count'],
                comment_count=stats['comment_count'],
                publish_time=stats['publish_time'],
                is_shorts=stats['is_shorts']
            )
            data = self.api_manager.get_comments(video_id)
            if data is None:
                continue
            for comment in data:
                self.db_manager.upsert_comments(
                    video_id=video_id,
                    author=comment['author'],
                    text=comment['text'],
                    like_count=comment['like_count']
                )
        return video_ids[:self.count]
    
    def save_channel_information(self):
        results = self.api_manager.get_channel_information()
        with open(self.ChannelInfo_filepath, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)

    def update_video_ids(self):
        results = self.api_manager.get_videoIds()
        for row in results:
            self.db_manager.upsert_videoIds(
                video_id=row["video_id"], 
                publish_time=row["publish_time"]
                )