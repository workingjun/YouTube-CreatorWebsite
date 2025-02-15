from src.app.database.mysql_channel_info import ChannelInfoManager
from src.app.database.mysql_about_links import LinksManager
from src.app.database.mysql_video_manager import VideoDataManager
from src.app.database.mysql_video_manager import VideoIdManager

class MySQLYouTubeDB(VideoDataManager, VideoIdManager, ChannelInfoManager, LinksManager):
    """댓글과 비디오 데이터를 모두 관리하는 클래스"""
    pass