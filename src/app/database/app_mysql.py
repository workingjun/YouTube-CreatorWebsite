from src.app.database.mysql_channel_info import ChannelInfoManager
from src.app.database.mysql_about_links import LinksManager
from src.app.database.mysql_video import VideoDataManager, VideoIdManager
from src.app.database.interface.channel_info import IChannelInfoManager
from src.app.database.interface.links import ILinksManager
from src.app.database.interface.video import IVideoDataManager, IVideoIdManager 
from src.app.database.db_manager import MysqlSSHManager

class MySQLYouTubeDB:
    def __init__(self, chinfo: IChannelInfoManager, links: ILinksManager, videoDt: IVideoDataManager, videoId: IVideoIdManager):
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
        vid_id = VideoIdManager(db_core)

        return MySQLYouTubeDB(
            chinfo=ch,
            videoDt=vid,
            links=link,
            videoId=vid_id
        )
    
