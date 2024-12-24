import os
from ftplib import FTP
from threading import Thread

class FTPmanager:
    def __init__(self, ftp_server, ftp_user, ftp_password):
        self.ftp_server = ftp_server
        self.ftp_user = ftp_user
        self.ftp_password = ftp_password

    def connect_ftp(self):
        ftp = FTP(self.ftp_server)
        ftp.login(user=self.ftp_user, passwd=self.ftp_password)
        return ftp

    def upload_file(self, local_path, remote_path):
        try:
            ftp = self.connect_ftp()
            with open(local_path, "rb") as file:
                ftp.storbinary(f"STOR {remote_path}", file)
            print(f"파일 업로드 성공: {local_path} -> {remote_path}")
        except Exception as e:
            print(f"파일 업로드 실패: {local_path}, 오류: {e}")
        finally:
            ftp.quit()

    def upload_directory(self, local_path, remote_path):
        # 원격 디렉토리 생성
        ftp = self.connect_ftp()
        try:
            ftp.mkd(remote_path)
            print(f"디렉터리 생성: {remote_path}")
        except Exception:
            print(f"디렉터리 이미 존재 또는 생성 오류: {remote_path}")
        finally:
            ftp.quit()

        threads = []

        # 로컬 디렉터리의 모든 항목 탐색
        for item in os.listdir(local_path):
            local_item_path = os.path.join(local_path, item)
            remote_item_path = f"{remote_path}/{item}"

            if os.path.isfile(local_item_path):
                # 파일 업로드를 별도의 스레드로 실행
                thread = Thread(target=self.upload_file, args=(local_item_path, remote_item_path))
                thread.start()
                threads.append(thread)
            elif os.path.isdir(local_item_path):
                # 디렉토리 업로드는 재귀적으로 호출
                self.upload_directory(local_item_path, remote_item_path)

        # 모든 스레드가 완료될 때까지 대기
        for thread in threads:
            thread.join()

    def upload_to_ftp(self, directory_path, upload_dir):
        self.upload_directory(directory_path, upload_dir)
        print("모든 파일 업로드 완료!")
