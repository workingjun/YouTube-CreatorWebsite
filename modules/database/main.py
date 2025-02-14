from modules.database.ChannelInfo import ChannelInfoManager
from modules.database.Links import LinksManager
from modules.database.VideoData import VideoDataManager
from modules.database.VideoIds import VideoIdManager

class MySQLYouTubeDB(VideoDataManager, VideoIdManager, ChannelInfoManager, LinksManager):
    """댓글과 비디오 데이터를 모두 관리하는 클래스"""
    def __init__(self):
        super().__init__()