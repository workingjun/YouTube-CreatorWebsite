from modules.youtube import YouTubeManager
from modules.HTML import HtmlManager
from modules.FTP import TransFTP
from dotenv import load_dotenv
import os
from datetime import datetime


class Main:

    channelId = ["UCW945UjEs6Jm3rVNvPEALdg"]
    file_path = [
        "data/transfer_files/comments_data.json", 
        "data/transfer_files/comments.html", 
        "data/transfer_files/index.html"
        ]

    def run(self):
        load_dotenv("data/.env.google")
        current_time = datetime.now()
        if current_time.weekday() == 5 or current_time.weekday() == 6: 
            if current_time.hour == 1:
                api_key = os.getenv("api_key_update")
                print("json 업데이트")
                youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0])
                youtube_manager.save_videoId()
            else:
                api_key = os.getenv("api_key_always")
                youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0])
        else:    
            if current_time.hour == 6:
                api_key = os.getenv("api_key_update")
                print("json 업데이트")
                youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0])
                youtube_manager.save_videoId()
            else:
                api_key = os.getenv("api_key_always")
                youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0])
        html_manager = HtmlManager(youtube_manager)
        html_manager.save_index_to_file()
        ftp = TransFTP()
        ftp.upload_files_to_ftp("ftpupload.net", "if0_37728238", "junhee0890", self.file_path, "/htdocs/")

if __name__=="__main__":
    main = Main()
    main.run()
    
    