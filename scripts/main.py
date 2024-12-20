from modules.youtube import YouTubeManager
from modules.HTML import HtmlManager
from modules.FTP import upload_files_to_ftp
from dotenv import load_dotenv
import os
from datetime import datetime

class Main:

    os.chdir("C:\Windows\System32\YoutubeNotify")
    channelId = ["UCW945UjEs6Jm3rVNvPEALdg"]
    env_path = "youtube_data/.env.google"
    index_path = "youtube_data/transfer_files/"
        
    def YOUTUBE_MANAGER(self, count=5, flags=False):
        load_dotenv(self.env_path)
        api_key = os.getenv("api_key1")
        youtube_manager = YouTubeManager(api_key=api_key, channelID=self.channelId[0], count=count)
        if flags:
            youtube_manager.save_videoId()
        return youtube_manager

    def run(self):
        current_time = datetime.now()
        load_dotenv(self.env_path)
        ftp_pw = os.getenv("ftp_pw")
        if current_time.weekday() == 5 or current_time.weekday() == 6: 
            if current_time.hour == 13:
                youtube_manager = self.YOUTUBE_MANAGER(count=-1, flags=True)
            else:
                youtube_manager = self.YOUTUBE_MANAGER()
        else:    
            if current_time.hour == 18:
                youtube_manager = self.YOUTUBE_MANAGER(count=-1, flags=True)
            else:
                youtube_manager = self.YOUTUBE_MANAGER()
        html_manager = HtmlManager(youtube_manager)
        html_manager.save_index_to_file()

        upload_files_to_ftp("ftpupload.net", "if0_37760205", ftp_pw, self.index_path, "/htdocs/")
        

if __name__=="__main__":
    main = Main()
    main.run()

    
    
    
