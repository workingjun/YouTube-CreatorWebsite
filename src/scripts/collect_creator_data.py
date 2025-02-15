from googleapiclient.discovery import build
from src.config import get_api_key
from src.config import CHANNELID
from src.app.database import MySQLYouTubeDB
from src.modules import collect_creators
from src.modules import collect_creators_channelInfo
from src.modules import fetch_shorts_videos
from src.modules import fetch_all_playlists
from src.modules import fetch_all_playlist_items

def start_collect_creator_data():
    db_manager = MySQLYouTubeDB()
    db_manager.connect(ssh_flags=True)
    
    channel_name = input("[INPUT] Channel Name: ")
    
    collect_creators(db_manager, channel_name, 8)
    collect_creators_channelInfo(db_manager, channel_name, 8)
    
    youtube = build("youtube", "v3", developerKey=get_api_key(8))
    
    playlist_ids = fetch_all_playlists(youtube, CHANNELID["channel_name"])
    all_video_data_1 = fetch_all_playlist_items(youtube, playlist_ids)
    all_video_data1 = fetch_shorts_videos(youtube, CHANNELID["channel_name"])

    db_manager.upsert_videoIds(table_name=channel_name, video_ids_list=all_video_data1)
    
    db_manager.close()
