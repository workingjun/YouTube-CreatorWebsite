from config.api_config import get_api_key
from googleapiclient.discovery import build
from config.channelId import CHANNELID
from modules.database import MySQLYouTubeDB
from modules.links import collect_creators
from modules.youtube import YouTubeManager
from modules.youtube import fetch_shorts_videos
from modules.youtube import fetch_all_playlists
from modules.youtube import fetch_all_playlist_items

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
    
if __name__=="__main__":
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
