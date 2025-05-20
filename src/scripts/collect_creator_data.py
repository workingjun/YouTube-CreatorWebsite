from googleapiclient.discovery import build
from src.app.database import MySQLYouTubeDBFactory
from src.modules import collect_creators
from src.modules import collect_creators_channelInfo
from src.modules import fetch_shorts_videos
# from src.modules import fetch_all_playlists
# from src.modules import fetch_all_playlist_items
from src.utils.yamL import load_yaml

def start_collect_creator_data(channel_name):
    API_KEY = load_yaml("./config/api_config.dev.yaml")
    CHANNELID = load_yaml("./config/channel_id.dev.yaml")
    DB_CONFIG = load_yaml("./config/db_config.dev.yaml")["ssh"]

    db_manager = MySQLYouTubeDBFactory(DB_CONFIG)
    db_manager.db_core.connect()
    
    collect_creators(db_manager, channel_name, CHANNELID[channel_name], 8)
    collect_creators_channelInfo(db_manager, channel_name, CHANNELID[channel_name], 8)
    
    youtube = build("youtube", "v3", developerKey=API_KEY[8])
    
    # playlist_ids = fetch_all_playlists(youtube, CHANNELID[channel_name])
    # all_video_data = fetch_all_playlist_items(youtube, playlist_ids)
    all_video_data = fetch_shorts_videos(youtube, CHANNELID[channel_name])

    db_manager.videoId.upsert_data(channel_name, all_video_data)
    db_manager.db_core.close()
