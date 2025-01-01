from googleapiclient.discovery import build
from config.api_config import get_api_key
from scripts.youtubeAPI.API_ALL_VIDEO_IDs import fetch_all_playlist_items, fetch_all_playlists, fetch_shorts_videos
from DB.database import MySQLYouTubeDB
from config.channelid_config import CHANNELID

if __name__=="__main__":
    db_manager = MySQLYouTubeDB()
    db_manager.connect(ssh_flags=True)
    youtube = build("youtube", "v3", developerKey=get_api_key(1))
    #playlist_ids = fetch_all_playlists(youtube, "UCW945UjEs6Jm3rVNvPEALdg")
    #all_video_data = fetch_all_playlist_items(youtube, playlist_ids)
    all_video_data1 = fetch_shorts_videos(youtube, CHANNELID["보겸"])
    all_video_data2 = fetch_shorts_videos(youtube, CHANNELID["지식줄고양"])
    all_video_data3 = fetch_shorts_videos(youtube, CHANNELID["김럽미"])
    db_manager.upsert_videoIds(table_name="보겸TV", video_ids_list=all_video_data1)
    db_manager.upsert_videoIds(table_name="지식줄고양", video_ids_list=all_video_data2)
    db_manager.upsert_videoIds(table_name="김 럽미", video_ids_list=all_video_data3)
    db_manager.close()