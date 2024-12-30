from DB.database import MySQLYouTubeDB
from config.api_config import api_key
from scripts.youtube import YouTubeManager

if __name__=="__main__":
    db_manager = MySQLYouTubeDB()
    db_manager.connect(ssh_flags=True)
    youtube_manager = YouTubeManager(
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        api_key=api_key[3]   
        )
    youtube_manager.save_channel_information()
    youtube_manager.collect_data(
        update_video_ids=False, 
        db_manager=db_manager
        )
    db_manager.close()