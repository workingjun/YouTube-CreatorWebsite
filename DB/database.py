import pymysql
from config.db_config import DB_COMFIG, SSH_HOST, SSH_PASSWORD, SSH_USER, MYSQL_HOST

class BaseDatabaseManager:
    _shared_connection = None
    _tunnel = None

    @staticmethod
    def start_ssh_tunnel():
        import sshtunnel
        if BaseDatabaseManager._tunnel is None:
            BaseDatabaseManager._tunnel = sshtunnel.SSHTunnelForwarder(
                (SSH_HOST, 22),
                ssh_username=SSH_USER,
                ssh_password=SSH_PASSWORD,
                remote_bind_address=(MYSQL_HOST, 3306),
                local_bind_address=('127.0.0.1', 0)  # 동적 포트
            )
            BaseDatabaseManager._tunnel.start()
            print(f"[SUCCESS] SSH 터널 연결 성공: {BaseDatabaseManager._tunnel.local_bind_port}")
    
    @staticmethod
    def stop_ssh_tunnel():
        if BaseDatabaseManager._tunnel is not None:
            BaseDatabaseManager._tunnel.stop()
            BaseDatabaseManager._tunnel = None
            print("[SUCCESS] SSH 터널 연결 종료")
        
    def connect(self, ssh_flags: bool=False):
        if ssh_flags:
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
            #self.stop_ssh_tunnel()
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
            print("[SUCCESS] Batch query executed.")
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
        
    def fetch_one(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()  # 첫 번째 행만 가져옴
            return result
        except pymysql.MySQLError as e:
            print(f"[ERROR] Fetching data failed: {e}")
            return None
    
    def execute_query_many(self, query, data_list):
        try:
            self.cursor.executemany(query, data_list)
            self.conn.commit()  # Commit the transaction
            print("[SUCCESS] Batch query executed.")
        except Exception as e:
            self.conn.rollback()  # Rollback the transaction in case of an error
            print(f"[ERROR] Batch query failed: {e}")

# 아래 Manager 클래스들은 기존 코드와 동일합니다
class VideoDataManager(BaseDatabaseManager):
    """비디오 데이터를 관리하는 클래스"""
    def upsert_videoData(self, video_data_list):
        data_list = [
            (
                video["video_id"],
                video["title"],
                video["view_count"],
                video["like_count"],
                video["comment_count"],
                video["publish_time"],
                video["is_shorts"],
            )
            for video in video_data_list
        ]
        print(f"[INFO] Inserting or updating video data")
        
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
        self.execute_query_many(sql, data_list)
        print(f"[SUCCESS] Video data processed")

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

        # 기존 데이터 조회
        sql_check = "SELECT text, like_count FROM comments WHERE video_id = %s AND author = %s"
        existing_data = self.fetch_one(sql_check, (video_id, author))

        # 데이터가 존재하고 동일한 경우 건너뜁니다
        if existing_data:
            if (existing_data == (text, like_count)):
                print(f"[INFO] Skipping update for comment by {author} on video_id: {video_id}, data is identical.")
                return
            
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
    def upsert_videoIds(self, video_ids_list):
        print(f"[INFO] Inserting or updating video IDs:")
        data_list = [
            (
                video_id["video_id"],
                video_id["publish_time"]
            )
            for video_id in video_ids_list
        ]
        sql = """
        INSERT INTO videoId (video_id, publish_time)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            video_id = VALUES(video_id),
            publish_time = VALUES(publish_time)
        """
        self.execute_query_many(sql, data_list)
        print(f"[SUCCESS] Video ID processed")

    def fetch_videoIds(self):
        print("[INFO] Fetching all video IDs")
        sql = "SELECT * FROM videoId ORDER BY publish_time DESC"
        result = self.fetch_all(sql)
        print("[SUCCESS] Fetched all video IDs")
        return result
           
class MySQLYouTubeDB(CommentDataManager, VideoDataManager, VideoIdManager):
    """댓글과 비디오 데이터를 모두 관리하는 클래스"""
    pass
