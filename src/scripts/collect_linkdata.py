from src.app.database import MySQLYouTubeDBFactory
from src.modules import collect_creators
from src.modules import ChromeDriverManager
from src.utils.yamL import load_yaml

def start_collect_link_data():
    CHANNELID = load_yaml("./config/channel_id.dev.yaml")
    DB_CONFIG = load_yaml("./config/db_config.dev.yaml")["ssh"]

    db_manager = MySQLYouTubeDBFactory(DB_CONFIG, True)
    db_manager.db_core.connect()
    manager = ChromeDriverManager()
    for channel_name, channel_id in CHANNELID.items():
        manager.start(
            url=f"https://www.youtube.com/channel/{channel_id}/about",
            headless=True, maximize=True
            )
        dictonary = collect_creators(manager.browser, channel_name)
        db_manager.links.upsert_data(channel_name, dictonary)