from DB.database import MySQLYouTubeDB
from config.api_config import api_key
from scripts.youtube import YouTubeManager

if __name__=="__main__":
    db_manager = MySQLYouTubeDB()
    db_manager.connect()
    youtube_manager = YouTubeManager(
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        api_key=api_key[1]   
    )
    youtube_manager.save_channel_information()
    youtube_manager.collect_data(db_manager=db_manager)
    db_manager.close()