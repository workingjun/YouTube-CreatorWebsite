from config.channelId import CHANNELID
from modules.youtube.youtube_manager import YouTubeManager
from modules.youtube.html_genertator import save_channel_index_to_file

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
        self.youtube_manager.collect_data(db_manager=db_manager, table_name=self.channelName, update_video_ids=update_video_ids)
        # Generate and save updated HTML file
        save_channel_index_to_file(output_path=index_path, table_name=self.channelName, db_manager=db_manager)