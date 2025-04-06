from src.app.database.mysql_channel_info import ChannelInfoManager
from src.app.database.mysql_about_links import LinksManager
from src.app.database.mysql_video import VideoDataManager
from src.app.database.mysql_video import VideoIdManager
from src.app.database.db_manager import MysqlSSHManager

class MySQLYouTubeDB:
    def __init__(self, chinfo: ChannelInfoManager, links: LinksManager, videoDt: VideoDataManager, videoId: VideoIdManager):
        self.chinfo = chinfo
        self.links = links
        self.videoDt = videoDt
        self.videoId = videoId

class MySQLYouTubeDBFactory:
    @staticmethod
    def create(db_config: dict, ssh_flags: bool) -> MySQLYouTubeDB:
        db_core = MysqlSSHManager(db_config, ssh_flags)

        ch = ChannelInfoManager(db_core)
        vid = VideoDataManager(db_core)
        link = LinksManager(db_core)

        return MySQLYouTubeDB(
            channel_info=ch,
            video_data=vid,
            links=link
        )