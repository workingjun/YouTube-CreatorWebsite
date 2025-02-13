from modules import collect_creators
from modules.database import MySQLYouTubeDB
from modules import ChromeDriverManager
from config.channelId import CHANNELID

if __name__=='__main__':
    db_manager = MySQLYouTubeDB()
    db_manager.connect(ssh_flags=True)
    manager = ChromeDriverManager()
    for channel_name, channel_id in CHANNELID.items():
        manager.start(
            url=f"https://www.youtube.com/channel/{channel_id}/about",
            headless=True, maximize=True
            )
        dictonary = collect_creators(manager.browser, channel_name)
        db_manager.upsert_Links(table_name=channel_name, links_list=dictonary)