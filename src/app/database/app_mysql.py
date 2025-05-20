from src.app.database.db_manager import MysqlSSHManager
from src.app.database.mysql_channel_info import ChannelInfoManager
from src.app.database.mysql_links import LinksManager
from src.app.database.mysql_video import VideoDataManager, VideoIdManager
from src.app.database.interface.channel_info import IChannelInfoManager
from src.app.database.interface.links import ILinksManager
from src.app.database.interface.video import IVideoDataManager, IVideoIdManager 

class MySQLYouTubeDB:
    def __init__(self, db_core: MysqlSSHManager, chinfo: IChannelInfoManager, links: ILinksManager, videoDt: IVideoDataManager, videoId: IVideoIdManager):
        self.db_core = db_core
        self.chinfo = chinfo
        self.links = links
        self.videoDt = videoDt
        self.videoId = videoId

def MySQLYouTubeDBFactory(db_config: dict, ssh_flags: bool=False) -> MySQLYouTubeDB:
    db_core = MysqlSSHManager(db_config, ssh_flags)

    ch = ChannelInfoManager(db_core)
    vid = VideoDataManager(db_core)
    link = LinksManager(db_core)
    vid_id = VideoIdManager(db_core)

    return MySQLYouTubeDB(
        db_core=db_core,
        chinfo=ch,
        videoDt=vid,
        links=link,
        videoId=vid_id
    )
    
