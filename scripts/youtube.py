from DB.database import CommentDataManager, CombinedDataManager, VideoIdManager
from scripts.youtubeAPI.api_manager import YoutubeApiManager
from scripts.utils.utils import DBManager
import json

class YouTubeManager:
    def __init__(self, api_key, channelID=None, channel_name=None, finish_all_video_ids:bool=False):
        self.ChannelInfo_filepath = "./json/ChannelInfo.json"
        self.count = -1 if finish_all_video_ids else 5
        self.api_manager = YoutubeApiManager(
            api_key=api_key, 
            channelID=channelID, 
            channel_name=channel_name
        )
        self.db_manager = DBManager(
            Comments=CommentDataManager(),
            VideoId=VideoIdManager(),
            Combine=CombinedDataManager()
        )

    def collect_data(self):
        video_ids = [row["video_id"] for row in self.db_manager.VideoId.fetch_videoIds()]
        for video_id in video_ids[:self.count]:
            stats = self.api_manager.get_video_statistics(video_id)
            if stats is None:
                continue
            self.db_manager.VideoId.upsert_videoId(
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
                self.db_manager.Comments.upsert_comments(
                    video_id=video_id,
                    author=comment['author'],
                    text=comment['text'],
                    like_count=comment['like_count']
                )
        return video_ids[:self.count]
    
    def save_channel_information(self):
        result = self.api_manager.get_channel_information()
        with open(self.ChannelInfo_filepath, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
