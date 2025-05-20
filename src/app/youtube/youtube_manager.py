from src.app.youtube.api_manager import YoutubeApiManager
from src.app.database.app_mysql import MySQLYouTubeDB

class YouTubeManager:
    def __init__(self, api_key, clannel_id=None, channel_name=None):
        self.api_manager = YoutubeApiManager(
            api_key=api_key, 
            clannel_id=clannel_id, 
            channel_name=channel_name
        )

    def collect_videoData(self, db_manager: MySQLYouTubeDB, video_ids, table_name):
        for video_id in video_ids:
            stats = self.api_manager.get_video_statistics(video_id)
            if stats is None:
                continue
            db_manager.videoDt.upsert_data(table_name, stats)

    def collect_videoId(self, db_manager: MySQLYouTubeDB, table_name, update_video_ids:bool=False):
        if update_video_ids:
            video_ids_list = self.api_manager.get_videoIds() 
            db_manager.videoId.upsert_data(table_name, video_ids_list)
            video_ids = [row['video_id'] for row in video_ids_list]
        else:
            video_ids = [row['video_id'] for row in db_manager.videoId.fetch_all(table_name)] 
        
        return video_ids

    def collect_channelInfo(self, db_manager: MySQLYouTubeDB):
        results = self.api_manager.get_channel_information()
        db_manager.chinfo.upsert_data(results)
