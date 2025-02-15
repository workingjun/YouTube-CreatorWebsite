from googleapiclient.discovery import build
from src.config.api_config import get_api_key
from src.config.channelId import CHANNELID
from src.app.youtube.youtube_manager import YouTubeManager

def collect_creators(db_manager, channel_name, api_key_num):
    youtube_manager = YouTubeManager(
        channelID=CHANNELID[channel_name],
        api_key=get_api_key(api_key_num)
        )
    youtube_manager.collect_data(
        update_video_ids=False, 
        db_manager=db_manager,
        table_name=channel_name
        )
    
def collect_creators_channelInfo(db_manager, channel_name, api_key_num):
    youtube_manager = YouTubeManager(
        channelID=CHANNELID[channel_name],
        api_key=get_api_key(api_key_num)
        )
    youtube_manager.collect_channelInfo(db_manager)