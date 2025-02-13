from modules.youtube.api_manager import YoutubeApiManager
from modules.database.main import MySQLYouTubeDB

class YouTubeManager:
    def __init__(self, api_key, channelID=None, channel_name=None):
        self.api_manager = YoutubeApiManager(
            api_key=api_key, 
            channelID=channelID, 
            channel_name=channel_name
        )
    
    def collect_data(self, db_manager: MySQLYouTubeDB, table_name, update_video_ids:bool=False):
        if update_video_ids:
            video_ids_list = self.api_manager.get_videoIds() 
            db_manager.upsert_videoIds(table_name=table_name, video_ids_list=video_ids_list)
            video_ids = [row['video_id'] for row in video_ids_list]
        else:
            video_ids = [row['video_id'] for row in db_manager.fetch_videoIds(table_name=table_name)] 
            
        results = self.api_manager.get_channel_information()
        db_manager.upsert_channel_info(data=results)

        video_data = []
        for video_id in video_ids:
            stats = self.api_manager.get_video_statistics(video_id)
            if stats is None:
                continue
            #video_data.append(stats)
            db_manager.upsert_videoData(table_name, stats)

        #batch_size = 100  # 한 번에 처리할 데이터 크기
        #for i in range(0, len(video_data), batch_size):
        #    batch = video_data[i:i+batch_size]
        #    db_manager.upsert_videoData(table_name=table_name, video_data=batch)

    def collect_channelInfo(self, db_manager: MySQLYouTubeDB):
        results = self.api_manager.get_channel_information()
        db_manager.upsert_channel_info(data=results)