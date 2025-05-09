from src.config.channelId import CHANNELID
from src.app.youtube.youtube_manager import YouTubeManager
from src.app.youtube.html_genertator import save_channel_index_to_file

# YouTube Creator Website class
class YOUTUBECreatorWebsite:
    def __init__(self, channelName, api_key):
        self.channelName = channelName
        self.channelID = CHANNELID[f"{self.channelName}"]
        self.api_key = api_key
        self.youtube_manager = YouTubeManager(api_key=self.api_key, channelID=self.channelID)

    def update_index_html(self, index_path, db_manager, update_video_ids:bool):
        """Updates the index.html with the latest channel data"""
        # Collect partial video data
        self.youtube_manager.collect_videoData(db_manager, self.channelName)
        self.youtube_manager.collect_videoId(db_manager, self.channelName, update_video_ids)
        self.youtube_manager.collect_channelInfo(db_manager)
        # Generate and save updated HTML file
        save_channel_index_to_file(index_path, self.channelName, db_manager)