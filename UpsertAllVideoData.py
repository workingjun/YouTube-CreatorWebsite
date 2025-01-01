from DB.database import MySQLYouTubeDB
from config.api_config import get_api_key
from scripts.youtube import YouTubeManager
from config.channelid_config import CHANNELID


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
    #collect_creators("보겸", 3)
    #collect_creators("김럽미", 3)
    collect_creators("지식줄고양", 3)
    db_manager.close()