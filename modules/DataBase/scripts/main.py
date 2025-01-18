from modules.database.scripts.ChannelInfo import ChannelInfoManager
from modules.database.scripts.Links import LinksManager
from modules.database.scripts.VideoData import VideoDataManager
from modules.database.scripts.VideoIds import VideoIdManager

class MySQLYouTubeDB(VideoDataManager, VideoIdManager, ChannelInfoManager, LinksManager):
    """댓글과 비디오 데이터를 모두 관리하는 클래스"""
    pass