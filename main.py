from modules.youtube import YouTubeManager
from modules.HTML import HtmlManager
from modules.Email import EmailManager
from modules.News import NewsManager
from modules.Chrome import ChromeManager
from time import sleep
from dotenv import load_dotenv
import os

if __name__=="__main__":
    Body=''; channelId = {"우정잉":'UCW945UjEs6Jm3rVNvPEALdg',}
    load_dotenv("./.env")
    email = os.getenv("email")
    sender_password = os.getenv("sender_password")
    api_key = os.getenv("api_key")
    for name in channelId:
        youtube_manager = YouTubeManager(api_key, channelId[name])
        html_manager = HtmlManager(youtube_manager)
        Body += html_manager.htmlrun()
    template = html_manager.load_template()
    html = template.format(body=Body)
    email_manager = EmailManager()
    email_manager.SendEmail(sender_email=email, sender_password=sender_password,
        recipient_email=email, subject='유튜브 분석 정보', body=html)
    chrome_manager = ChromeManager(url="https://news.google.com/home?hl=ko&gl=KR&ceid=KR:ko")
    chrome_manager.process_Chrome(); sleep(5)
    news_manager = NewsManager(chrome_manager)
    email_manager.SendEmail(sender_email=email, sender_password=sender_password,
        recipient_email=email, subject='오늘의 헤드라인', body=news_manager.result)
    sleep(10); chrome_manager.terminate_chrome_process()

    
