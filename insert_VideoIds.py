from googleapiclient.discovery import build
from config.api_config import api_key
from scripts.youtubeAPI.API_ALL_VIDEO_IDs import fetch_all_playlist_items, fetch_all_playlists 
from DB.database import MySQLYouTubeDB

if __name__=="__main__":
    youtube = build("youtube", "v3", developerKey=api_key[0])
    playlist_ids = fetch_all_playlists(youtube, "UCW945UjEs6Jm3rVNvPEALdg")
    all_video_data = fetch_all_playlist_items(youtube, playlist_ids)

    db_manager = MySQLYouTubeDB()
    db_manager.connect()
    for video_data in all_video_data:
        db_manager.upsert_videoId(
            video_id=video_data["video_id"], 
            publish_time=video_data["published_time"]
            )
    db_manager.close()