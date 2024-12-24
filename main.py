import os
os.chdir("D:\YoutubeNotify")
from dotenv import load_dotenv
from datetime import datetime
from scripts.youtube import YouTubeManager
from scripts.HTML import HtmlManager
from scripts.DataBase import DatabaseManager
from scripts.FTP import FTPmanager

class YOUTUBECreatorWebsite:
    def __init__(self, channelID, index_path, remote_path, api_key, db_config, ftp_config):
        self.channelID = channelID
        self.api_key = api_key
        self.index_path = index_path
        self.remote_path = remote_path
        self.db_manager = DatabaseManager(**db_config)
        self.ftp_manager = FTPmanager(**ftp_config)

    def get_youtube_manager(self, count=5, flags=False):
        """YouTubeManager 객체 생성"""
        youtube_manager = YouTubeManager(api_key=self.api_key, channelID=self.channelID, count=count)
        if flags:
            youtube_manager.save_videoId(page=1, db_manager=self.db_manager)
            # youtube_manager.save_videoId_from_playlist(db_manager=self.db_manager)
        return youtube_manager

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

        # FTP 업로드
        self.ftp_manager.upload_to_ftp(self.index_path, "/friendshiping.ct.ws/htdocs")
        print("파일 업로드 완료.")

if __name__ == "__main__":
    # 환경 변수 파일 로드
    env_files = ["secrets/.env.DB", "secrets/.env.ftp", "secrets/.env.google"]
    for file in env_files:
        if os.path.exists(file):
            load_dotenv(file)
        else:
            raise FileNotFoundError(f"환경 변수 파일이 존재하지 않습니다: {file}")

    # 환경 변수 가져오기
    required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "ftp_pw", "ftp_name", 
                         "api_key1", "api_key2", "api_key3", "api_key4", "api_key5"]
    env_values = {var: os.getenv(var) for var in required_env_vars}

    if not all(env_values.values()):
        raise ValueError(f"필수 환경 변수 누락: {', '.join([k for k, v in env_values.items() if not v])}")

    # 설정 구성
    db_config = {
        "host": env_values["DB_HOST"],
        "user": env_values["DB_USER"],
        "password": env_values["DB_PASSWORD"],
        "database": env_values["DB_NAME"],
    }
    ftp_config = {
        "ftp_server": "ftpupload.net",
        "ftp_user": env_values["ftp_name"],
        "ftp_password": env_values["ftp_pw"],
    }

    # Main 클래스 실행
    youtube_creator1 = YOUTUBECreatorWebsite(
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        index_path= "./transfer_files/",
        remote_path= "/friendshiping.ct.ws/htdocs/",
        api_key=env_values["api_key2"],
        db_config=db_config,
        ftp_config=ftp_config,
    )
    youtube_creator1.Update_Website()
