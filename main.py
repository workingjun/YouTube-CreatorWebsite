from modules.youtube import YouTubeManager
from modules.HTML import HtmlManager
from modules.FTP import TransFTP
from dotenv import load_dotenv
import os
from datetime import datetime


class Main:

    channelId = ["UCW945UjEs6Jm3rVNvPEALdg"]
    file_path = [
        "youtube_data/transfer_files/comments_data.json", 
        "youtube_data/transfer_files/comments.html", 
        "youtube_data/transfer_files/index.html"
        ]
    env_path = "youtube_data/.env.google"

    def case1(self):
        load_dotenv(self.env_path)
        try:    
            api_key = os.getenv("api_key_always")
            youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0], count=-1)
        except:
            api_key = os.getenv("api_key_update")
            youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0], count=-1)
        youtube_manager.save_videoId()
        return youtube_manager
        
    def case2(self):
        load_dotenv(self.env_path)
        try:    
            api_key = os.getenv("api_key_always")
            youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0], count=5)
        except:
            api_key = os.getenv("api_key_update")
            youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0], count=5)
        return youtube_manager

    def run(self):
        current_time = datetime.now()
        if current_time.weekday() == 5 or current_time.weekday() == 6: 
            if current_time.hour == 13:
                youtube_manager = self.case1()
            else:
                youtube_manager = self.case2()
        else:    
            if current_time.hour == 18:
                youtube_manager = self.case1()
            else:
                youtube_manager = self.case2()
        html_manager = HtmlManager(youtube_manager)
        html_manager.save_index_to_file()
        ftp = TransFTP()
        ftp.upload_files_to_ftp("ftpupload.net", "if0_37728238", "junhee0890", self.file_path, "/htdocs/")

if __name__=="__main__":
    main = Main()
    main.run()
    
    