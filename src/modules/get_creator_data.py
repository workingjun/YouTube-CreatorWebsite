from src.app.youtube.youtube_manager import YouTubeManager

def collect_creators(db_manager, channel_name, channel_id, api_key):
    youtube_manager = YouTubeManager(
        channelID=channel_id[channel_name],
        api_key=api_key
        )
    youtube_manager.collect_data(
        update_video_ids=False, 
        db_manager=db_manager,
        table_name=channel_name
        )
    
def collect_creators_channelInfo(db_manager, channel_name, channel_id, api_key):
    youtube_manager = YouTubeManager(
        channelID=channel_id[channel_name],
        api_key=api_key
        )
    youtube_manager.collect_channelInfo(db_manager)