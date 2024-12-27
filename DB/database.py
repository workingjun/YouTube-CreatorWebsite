import mysql.connector
from config.db_config import db_config

class BaseDatabaseManager:
    """공통 데이터베이스 작업을 관리하는 부모 클래스"""
    _shared_connection = None  # 공유 데이터베이스 연결

    def __init__(self):
        if BaseDatabaseManager._shared_connection is None:
            # 공유 데이터베이스 연결 생성
            BaseDatabaseManager._shared_connection = mysql.connector.connect(**db_config)
        self.conn = BaseDatabaseManager._shared_connection
        self.cursor = self.conn.cursor(dictionary=True)

    def close(self):
        """데이터베이스 연결 종료 (공유 연결 닫기)"""
        if BaseDatabaseManager._shared_connection:
            BaseDatabaseManager._shared_connection.close()
            BaseDatabaseManager._shared_connection = None

    def execute_query(self, query, values=None):
        """쿼리를 실행하고 커밋"""
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f"[Error] Query execution failed: {e}")

    def fetch_all(self, query, values=None):
        """모든 결과를 가져오는 메서드"""
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[Error] Fetching data failed: {e}")
            return []

class VideoDataManager(BaseDatabaseManager):
    """비디오 데이터를 관리하는 클래스"""
    def upsert_videoData(self, video_id, title, view_count, like_count, comment_count, publish_time, is_shorts):
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

    def fetch_all_videoData(self):
        sql = "SELECT * FROM videoData"
        return self.fetch_all(sql)

class CommentDataManager(BaseDatabaseManager):
    """댓글 데이터를 관리하는 클래스"""
    def upsert_comments(self, video_id, author, text, like_count):
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

    def fetch_comments(self, video_id):
        sql = "SELECT author, text, like_count, created_at FROM comments WHERE video_id = %s"
        return self.fetch_all(sql, (video_id,))
    
class VideoIdManager(BaseDatabaseManager):
    """비디오 아이디를 관리하는 클래스"""
    def upsert_videoId(self, video_id, publish_time):
        sql = """
        INSERT INTO videoId (video_id, publish_time)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            video_id = VALUES(video_id, publish_time)
        """
        values = (video_id, publish_time)
        self.execute_query(sql, values)

    def fetch_videoIds(self):
        sql = "SELECT * FROM videoId ORDER BY publish_time DESC"
        return self.fetch_all(sql)
           
class CombinedDataManager(CommentDataManager, VideoDataManager):
    """댓글과 비디오 데이터를 모두 관리하는 클래스"""
    pass