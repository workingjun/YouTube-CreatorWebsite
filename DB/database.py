import pymysql
from config.db_config import DB_COMFIG, SSH_HOST, SSH_PASSWORD, SSH_USER, MYSQL_HOST
import sshtunnel

class BaseDatabaseManager:
    _shared_connection = None
    _tunnel = None

    @staticmethod
    def start_ssh_tunnel():
        if BaseDatabaseManager._tunnel is None:
            BaseDatabaseManager._tunnel = sshtunnel.SSHTunnelForwarder(
                (SSH_HOST, 22),
                ssh_username=SSH_USER,
                ssh_password=SSH_PASSWORD,
                remote_bind_address=(MYSQL_HOST, 3306),
                local_bind_address=('127.0.0.1', 0)  # 동적 포트
            )
            BaseDatabaseManager._tunnel.start()
            print(f"SSH 터널 연결 성공: {BaseDatabaseManager._tunnel.local_bind_port}")

    @staticmethod
    def stop_ssh_tunnel():
        if BaseDatabaseManager._tunnel is not None:
            BaseDatabaseManager._tunnel.stop()
            BaseDatabaseManager._tunnel = None
            print("SSH 터널 연결 종료")
        
    def connect(self):
        print("[INFO] Starting SSH tunnel...")
        self.start_ssh_tunnel()
        DB_COMFIG["port"] = BaseDatabaseManager._tunnel.local_bind_port
        print(f"[INFO] SSH tunnel started at local port {BaseDatabaseManager._tunnel.local_bind_port}")
        try:
            if BaseDatabaseManager._shared_connection is None:
                BaseDatabaseManager._shared_connection = pymysql.connect(**DB_COMFIG)
            self.conn = BaseDatabaseManager._shared_connection
            self.cursor = self.conn.cursor()
            print("[SUCCESS] MySQL connection established")
        except pymysql.MySQLError as e:
            print(f"[ERROR] MySQL connection failed: {e}")
            self.stop_ssh_tunnel()
            raise

    def close(self):
        """데이터베이스 연결 종료 (공유 연결 닫기)"""
        if BaseDatabaseManager._shared_connection:
            BaseDatabaseManager._shared_connection.close()
            BaseDatabaseManager._shared_connection = None
        self.stop_ssh_tunnel()

    def execute_query(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
        except pymysql.OperationalError as e:
            print(f"[OperationalError] Query execution failed: {e}")
            self.__init__()
        except pymysql.MySQLError as e:
            print(f"[MySQLError] Query execution failed: {e}")

    def fetch_all(self, query, values=None):
        """모든 결과를 가져오는 메서드"""
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"[Error] Fetching data failed: {e}")
            return []

# 아래 Manager 클래스들은 기존 코드와 동일합니다
class VideoDataManager(BaseDatabaseManager):
    """비디오 데이터를 관리하는 클래스"""
    def upsert_videoData(self, video_id, title, view_count, like_count, comment_count, publish_time, is_shorts):
        print(f"[INFO] Inserting or updating video data for video_id: {video_id}")
        sql = """
        INSERT INTO videoData (video_id, title, view_count, like_count, comment_count, publish_time, is_shorts)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            view_count = VALUES(view_count),
            like_count = VALUES(like_count),
            comment_count = VALUES(comment_count),
            publish_time = VALUES(publish_time),
            is_shorts = VALUES(is_shorts)
        """
        values = (video_id, title, view_count, like_count, comment_count, publish_time, is_shorts)
        self.execute_query(sql, values)
        print(f"[SUCCESS] Video data processed for video_id: {video_id}")

    def fetch_all_videoData(self):
        print("[INFO] Fetching all video data")
        sql = "SELECT * FROM videoData"
        result = self.fetch_all(sql)
        print("[SUCCESS] Fetched all video data")
        return result

class CommentDataManager(BaseDatabaseManager):
    """댓글 데이터를 관리하는 클래스"""
    def upsert_comments(self, video_id, author, text, like_count):
        print(f"[INFO] Inserting or updating comment for video_id: {video_id}, author: {author}")
        sql = """
        INSERT INTO comments (video_id, author, text, like_count)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            author = VALUES(author),
            text = VALUES(text),
            like_count = VALUES(like_count)
        """
        values = (video_id, author, text, like_count)
        self.execute_query(sql, values)
        print(f"[SUCCESS] Comment processed for video_id: {video_id}, author: {author}")

    def fetch_comments(self, video_id):
        print(f"[INFO] Fetching comments for video_id: {video_id}")
        sql = "SELECT author, text, like_count, created_at FROM comments WHERE video_id = %s"
        result = self.fetch_all(sql, (video_id,))
        print(f"[SUCCESS] Fetched comments for video_id: {video_id}")
        return result

class VideoIdManager(BaseDatabaseManager):
    """비디오 아이디를 관리하는 클래스"""
    def upsert_videoIds(self, video_id, publish_time):
        print(f"[INFO] Inserting or updating video ID: {video_id}")
        sql = """
        INSERT INTO videoId (video_id, publish_time)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            video_id = VALUES(video_id),
            publish_time = VALUES(publish_time)
        """
        values = (video_id, publish_time)
        self.execute_query(sql, values)
        print(f"[SUCCESS] Video ID processed: {video_id}")

    def fetch_videoIds(self):
        print("[INFO] Fetching all video IDs")
        sql = "SELECT * FROM videoId ORDER BY publish_time DESC"
        result = self.fetch_all(sql)
        print("[SUCCESS] Fetched all video IDs")
        return result
           
class MySQLYouTubeDB(CommentDataManager, VideoDataManager, VideoIdManager):
    """댓글과 비디오 데이터를 모두 관리하는 클래스"""
    pass
