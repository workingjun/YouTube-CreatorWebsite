from config.api_config import get_api_key
from googleapiclient.discovery import build
from config.channelId import CHANNELID
from modules.database import MySQLYouTubeDB
from modules import collect_creators
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
    
    #collect_creators(db_manager, "보겸TV", 8)
    #collect_creators(db_manager, "김 럽미", 8)
    #collect_creators(db_manager, "청산유수현 SUHYEON", 8)
    #collect_creators(db_manager, "지식줄고양", 8)
    collect_creators(db_manager, "우정잉", 8)

    #collect_creators_channelInfo(db_manager, "보겸TV", 8)
    #collect_creators_channelInfo(db_manager, "김 럽미", 8)
    #collect_creators_channelInfo(db_manager, "청산유수현 SUHYEON", 8)
    #collect_creators_channelInfo(db_manager, "지식줄고양", 8)
    #collect_creators_channelInfo(db_manager, "우정잉", 8)
    
    #youtube = build("youtube", "v3", developerKey=get_api_key(8))
    
    #playlist_ids = fetch_all_playlists(youtube, CHANNELID["우정잉"])
    #all_video_data_1 = fetch_all_playlist_items(youtube, playlist_ids)
    #all_video_data1 = fetch_shorts_videos(youtube, CHANNELID["우정잉"])

    #playlist_ids = fetch_all_playlists(youtube, CHANNELID["보겸"])
    #all_video_data_1 = fetch_all_playlist_items(youtube, playlist_ids)
    #all_video_data1 = fetch_shorts_videos(youtube, CHANNELID["보겸"])

    #playlist_ids = fetch_all_playlists(youtube, CHANNELID["지식줄고양"])
    #all_video_data_1 = fetch_all_playlist_items(youtube, playlist_ids)
    #all_video_data2 = fetch_shorts_videos(youtube, CHANNELID["지식줄고양"])

    #playlist_ids = fetch_all_playlists(youtube, CHANNELID["김럽미"])
    #all_video_data_1 = fetch_all_playlist_items(youtube, playlist_ids)
    #all_video_data3 = fetch_shorts_videos(youtube, CHANNELID["김럽미"])

    #playlist_ids = fetch_all_playlists(youtube, CHANNELID["우정잉"])
    #all_video_data_1 = fetch_all_playlist_items(youtube, playlist_ids)
    #all_video_data3 = fetch_shorts_videos(youtube, CHANNELID["우정잉"])
    
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data3)
    #db_manager.upsert_videoIds(table_name="보겸TV", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="지식줄고양", video_ids_list=all_video_data2)
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="김 럽미", video_ids_list=all_video_data3)
    
    db_manager.close()
