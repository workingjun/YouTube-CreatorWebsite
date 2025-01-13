from googleapiclient.discovery import build
from config.api_config import get_api_key
from config.channelid_config import CHANNELID
from modules.Link.external_link import collect_creators
from modules.DataBase.database import MySQLYouTubeDB
from modules.youtube.youtube_manager import YouTubeManager
from modules.youtubeAPI.API_ALL_VIDEO_IDs import fetch_all_playlist_items
from modules.youtubeAPI.API_ALL_VIDEO_IDs import fetch_shorts_videos
from modules.youtubeAPI.API_ALL_VIDEO_IDs import fetch_all_playlists

def collect_creators(channel_name, api_key_num):
    youtube_manager = YouTubeManager(
        channelID=CHANNELID[channel_name],
        api_key=get_api_key(api_key_num)
        )
    result = youtube_manager.save_channel_information(
        ChannelInfo_filepath=f"./json/{channel_name}_ChannelInfo.json"
        )
    youtube_manager.collect_data(
        update_video_ids=False, 
        db_manager=db_manager,
        table_name=result["title"]
        )

if __name__=="__main__":
    db_manager = MySQLYouTubeDB()
    db_manager.connect(ssh_flags=True)
    
    #collect_creators("보겸", 7)
    #collect_creators("김럽미", 7)
    #collect_creators("유수현", 7)
    #collect_creators("지식줄고양", 7)
    #collect_creators("우정잉", 8)
    
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
    
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data_1)
    #db_manager.upsert_videoIds(table_name="보겸TV", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="지식줄고양", video_ids_list=all_video_data2)
    #db_manager.upsert_videoIds(table_name="우정잉", video_ids_list=all_video_data1)
    #db_manager.upsert_videoIds(table_name="김 럽미", video_ids_list=all_video_data3)
    
    db_manager.close()
