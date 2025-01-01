from scripts.youtube import YouTubeManager
from scripts.html_genertator import HTMLGenerator
from config.channelid_config import CHANNELID

# YouTube Creator Website class
class YOUTUBECreatorWebsite:
    def __init__(self, channelName, api_key):
        self.channelName = channelName
        self.channelID = CHANNELID[f"{self.channelName}"]
        self.api_key = api_key
        self.youtube_manager = YouTubeManager(api_key=self.api_key, channelID=self.channelID)
        self.html_manager = HTMLGenerator()

    def update_index_html(self, index_path, ChannelInfo_filepath, db_manager, update_video_ids:bool):
        """Updates the index.html with the latest channel data"""
        # Save channel information
        results = self.youtube_manager.save_channel_information(ChannelInfo_filepath)
        # Collect partial video data
        self.youtube_manager.collect_data(db_manager=db_manager, table_name=results["title"], update_video_ids=update_video_ids)
        # Generate and save updated HTML file
        self.html_manager.save_index_to_file(output_path=index_path, table_name=results["title"], db_manager=db_manager)