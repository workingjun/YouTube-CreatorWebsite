from modules.links import collect_creators
from modules.database import MySQLYouTubeDB
from modules.links import ChromeDriverManager
from config.channelid_config import CHANNELID

db_manager = MySQLYouTubeDB()
db_manager.connect(ssh_flags=True)
with ChromeDriverManager(debug_flag=False, headless_flag=True) as manager:
    for channel_name, channel_id in CHANNELID.items():
        manager.get_url(
            url=f"https://www.youtube.com/channel/{channel_id}/about", 
            maximize_flag=True
            )
        dictonary = collect_creators(manager.get_browser(), channel_name)
        db_manager.upsert_Links(table_name=channel_name, links_list=dictonary)