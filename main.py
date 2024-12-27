from config.api_config import api_key
from datetime import datetime
from scripts.youtube import YouTubeManager
from scripts.html_genertator import HtmlManager
from DB.DataBase import DatabaseManager

class YOUTUBECreatorWebsite:
    def __init__(self, channelID, index_path, remote_path, api_key):
        self.channelID = channelID
        self.api_key = api_key
        self.index_path = index_path
        self.remote_path = remote_path
        self.db_manager = DatabaseManager()

    def get_youtube_manager(self, count=5, flags=False):
        if flags:
            YouTubeManager(
                api_key=self.api_key, 
                channelID=self.channelID, 
                count=count
                ).save_videoId(page=1, db_manager=self.db_manager)
        else:
            YouTubeManager(api_key=self.api_key, channelID=self.channelID, count=count)
        
    def Update_Website(self):
        """실행 로직"""
        current_time = datetime.now()

        # 주말과 평일 시간 설정
        if (current_time.weekday() >= 5 and current_time.hour == 13) or (current_time.weekday() < 5 and current_time.hour == 18):
            youtube_manager = self.get_youtube_manager(count=-1, flags=True)
        else:
            youtube_manager = self.get_youtube_manager()

        # HTML 생성 및 저장
        html_manager = HtmlManager(youtube_manager)
        html_manager.save_files(db_manager=self.db_manager)

if __name__ == "__main__":
    # Main 클래스 실행
    youtube_creator1 = YOUTUBECreatorWebsite(
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        index_path= "./transfer_files/",
        remote_path= "/friendshiping.ct.ws/htdocs/",
        api_key=api_key["api_num1"]
    )
    youtube_creator1.Update_Website()
