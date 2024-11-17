from modules.youtube import YouTubeManager
from modules.HTML import HtmlManager
from modules.Email import EmailManager
from modules.News import NewsManager
from modules.Chrome import ChromeManager
from time import sleep
from dotenv import load_dotenv
import os

from ftplib import FTP

def upload_file_to_ftp(ftp_server, ftp_user, ftp_password, file_path, upload_path):
    """
    FTP 서버에 파일 업로드
    :param ftp_server: FTP 서버 주소 (예: 'ftp.example.com')
    :param ftp_user: FTP 사용자명
    :param ftp_password: FTP 비밀번호
    :param file_path: 업로드할 로컬 파일 경로
    :param upload_path: FTP 서버의 업로드 경로
    """
    try:
        # FTP 연결
        ftp = FTP(ftp_server)
        ftp.login(user=ftp_user, passwd=ftp_password)
        print("FTP 연결 성공!")

        # 파일 전송
        with open(file_path, "rb") as file:
            ftp.storbinary(f"STOR {upload_path}", file)
        print(f"파일 업로드 성공: {file_path} -> {upload_path}")

        # FTP 연결 종료
        ftp.quit()
    except Exception as e:
        print(f"FTP 전송 중 오류 발생: {e}")


if __name__=="__main__":
    Body=''; channelId = {"우정잉":'UCW945UjEs6Jm3rVNvPEALdg'}
    load_dotenv("./.env.google")
    email = os.getenv("email")
    sender_password = os.getenv("sender_password")
    api_key = os.getenv("api_key")
    for name in channelId:
        youtube_manager = YouTubeManager(api_key, channelId[name])
        html_manager = HtmlManager(youtube_manager)
        Body += html_manager.htmlrun()
    template = html_manager.load_template()
    html = template.format(body=Body)
    html_file_path = "Youtube.html"
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(html)

    # 예제 사용법
    ftp_server = "ftpupload.net"
    ftp_user = "if0_37728238"
    ftp_password = "junhee0890"
    file_path = "./youtube.html"  # 업로드할 로컬 파일 경로
    upload_path = "/htdocs/index.html"  # FTP 서버 내 업로드 경로
    upload_file_to_ftp(ftp_server, ftp_user, ftp_password, file_path, upload_path)
    
