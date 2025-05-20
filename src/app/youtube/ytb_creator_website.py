from src.app.youtube.youtube_manager import YouTubeManager
from src.app.youtube.html_genertator import save_channel_index_to_file

# YouTube Creator Website class
class YOUTUBECreatorWebsite:
    def __init__(self, api_key, channel_name=None, channel_id=None):
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.youtube_manager = YouTubeManager(
            api_key=api_key, 
            channel_name=channel_name, 
            clannel_id=channel_id
            )

    def update_index_html(self, index_path, db_manager, update_video_ids:bool):
        """Updates the index.html with the latest channel data"""
        # Collect partial video data
        self.youtube_manager.collect_videoData(db_manager, self.channel_name)
        self.youtube_manager.collect_videoId(db_manager, self.channel_name, update_video_ids)
        self.youtube_manager.collect_channelInfo(db_manager)
        # Generate and save updated HTML file
        save_channel_index_to_file(index_path, self.channel_name, db_manager)