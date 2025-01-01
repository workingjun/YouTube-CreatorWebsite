import pymysql, time
from config.db_config import DB_CONFIG_DEFAULT, DB_CONFIG_SSH , SSH_HOST, SSH_PASSWORD, SSH_USER, MYSQL_HOST

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
            print(f"[SUCCESS] SSH tunnel connection established: {BaseDatabaseManager._tunnel.local_bind_port}")
    
    @staticmethod
    def stop_ssh_tunnel():
        if BaseDatabaseManager._tunnel is not None:
            BaseDatabaseManager._tunnel.stop()
            BaseDatabaseManager._tunnel = None
            print("[SUCCESS] SSH tunnel connection closed")
        
    def connect(self, ssh_flags: bool=False, retries: int=5, delay: int=5):
        if ssh_flags:
            print("[INFO] Starting SSH tunnel...")
            self.start_ssh_tunnel()
            DB_CONFIG_SSH["port"] = BaseDatabaseManager._tunnel.local_bind_port
            DB_COMFIG = DB_CONFIG_SSH
            print(f"[INFO] SSH tunnel started at local port {BaseDatabaseManager._tunnel.local_bind_port}")
        else:
            DB_COMFIG = DB_CONFIG_DEFAULT

        attempt = 0
        while attempt < retries:
            try:
                if BaseDatabaseManager._shared_connection is None:
                    print(f"[INFO] Attempting MySQL connection, attempt {attempt + 1} of {retries}")
                    BaseDatabaseManager._shared_connection = pymysql.connect(**DB_COMFIG)

                self.conn = BaseDatabaseManager._shared_connection
                self.cursor = self.conn.cursor()
                print("[SUCCESS] MySQL connection established")

                # 연결 후 주기적으로 연결 상태 확인 및 재연결 시도
                self.ensure_connection()  # 연결을 확인하고 필요 시 재연결

                return  # 성공하면 종료
            except pymysql.MySQLError as e:
                print(f"[ERROR] MySQL connection failed: {e}")
                attempt += 1
                if attempt < retries:
                    print(f"[INFO] Retrying in {delay} seconds...")
                    time.sleep(delay)  # 재시도 간 대기 시간
                else:
                    raise Exception(f"Failed to connect to MySQL after {retries} attempts.")  # 재시도 후 실패하면 예외 발생

    def close(self):
        """데이터베이스 연결 종료 (공유 연결 닫기)"""
        if BaseDatabaseManager._shared_connection:
            BaseDatabaseManager._shared_connection.close()
            BaseDatabaseManager._shared_connection = None
        self.stop_ssh_tunnel()

    def execute_query(self, query, values=None):
        try:
            self.ensure_connection()
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
            self.ensure_connection()
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"[Error] Fetching data failed: {e}")
            return []
        
    def fetch_one(self, query, values=None):
        try:
            self.ensure_connection()
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()  # 첫 번째 행만 가져옴
            return result
        except pymysql.MySQLError as e:
            print(f"[ERROR] Fetching data failed: {e}")
            return None
    
    def execute_query_many(self, query, data_list):
        try:
            self.ensure_connection()
            self.cursor.executemany(query, data_list)
            self.conn.commit()  # Commit the transaction
            print("[SUCCESS] Batch query executed.")
        except Exception as e:
            self.conn.rollback()  # Rollback the transaction in case of an error
            print(f"[ERROR] Batch query failed: {e}")

    def ensure_connection(self):
        """MySQL 연결이 유효한지 확인하고, 끊어진 경우 재연결"""
        try:
            # MySQL 연결 상태 확인 (reconnect=True 옵션으로 끊어진 경우 복구)
            self.conn.ping(reconnect=True)
        except pymysql.MySQLError as e:
            print("[ERROR] Connection lost. Reconnecting...")
            # 끊어진 경우 재연결 수행
            self.connect(ssh_flags=True if BaseDatabaseManager._tunnel else False)


class VideoDataManager(BaseDatabaseManager):
    """비디오 데이터를 관리하는 클래스"""

    def upsert_friendshiping_videoData(self, video_data_list):
        self.upsert_videoData("우정잉", video_data_list)
    
    def upsert_suhyeon_videoData(self, video_data_list):
        self.upsert_videoData("청산유수현 SUHYEON", video_data_list)

    def upsert_bokyem_videoData(self, video_data_list):
        self.upsert_videoData("보겸TV", video_data_list)

    def upsert_loveme_videoData(self, video_data_list):
        self.upsert_videoData("김 럽미", video_data_list)

    def upsert_cat_videoData(self, video_data_list):
        self.upsert_videoData("지식줄고양", video_data_list)
    
    def fetch_all_friendshiping_videoData(self):
        return self.fetch_all_videoData("우정잉")
    
    def fetch_all_suhyeon_videoData(self):
        return self.fetch_all_videoData("청산유수현 SUHYEON")
    
    def fetch_all_bokyem_videoData(self):
        return self.fetch_all_videoData("보겸TV")
    
    def fetch_all_loveme_videoData(self):
        return self.fetch_all_videoData("김 럽미")
    
    def fetch_all_cat_videoData(self):
        return self.fetch_all_videoData("지식줄고양")
    
    def upsert_videoData(self, table_name, video_data_list):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_VIDEO`"

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
        print(f"[INFO] Inserting or updating video data in {table_name}")
        
        sql = f"""
        INSERT INTO {table_name_safe} (video_id, title, view_count, like_count, comment_count, publish_time, is_shorts)
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
        print(f"[SUCCESS] Video data processed in {table_name}")
    
    def fetch_all_videoData(self, table_name):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_VIDEO`"
        print(f"[INFO] Fetching all video data from {table_name}")
        sql = f"SELECT * FROM {table_name_safe} ORDER BY publish_time DESC"
        result = self.fetch_all(sql)
        print(f"[SUCCESS] Fetched all video data from {table_name}")
        return result


class VideoIdManager(BaseDatabaseManager):
    """비디오 아이디를 관리하는 클래스"""
    
    def upsert_friendshiping_videoIds(self, video_data_list):
        self.upsert_videoIds("우정잉", video_data_list)
    
    def upsert_suhyeon_videoIds(self, video_data_list):
        self.upsert_videoIds("청산유수현 SUHYEON", video_data_list)

    def upsert_bokyem_videoIds(self, video_data_list):
        self.upsert_videoIds("보겸TV", video_data_list)

    def upsert_loveme_videoIds(self, video_data_list):
        self.upsert_videoIds("김 럽미", video_data_list)

    def upsert_cat_videoIds(self, video_data_list):
        self.upsert_videoIds("지식줄고양", video_data_list)
    
    def fetch_all_friendshiping_videoIds(self):
        return self.fetch_videoIds("우정잉")
    
    def fetch_all_suhyeon_videoIds(self):
        return self.fetch_videoIds("청산유수현 SUHYEON")
    
    def fetch_all_bokyem_videoIds(self):
        return self.fetch_videoIds("보겸TV")
    
    def fetch_all_loveme_videoIds(self):
        return self.fetch_videoIds("김 럽미")
    
    def fetch_all_cat_videoIds(self):
        return self.fetch_videoIds("지식줄고양")
    
    def upsert_videoIds(self, table_name, video_ids_list):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_IDS`"
        print(f"[INFO] Inserting or updating video IDs in {table_name}:")
        data_list = [
            (
                video_id["video_id"],
                video_id["publish_time"]
            )
            for video_id in video_ids_list
        ]
        sql = f"""
        INSERT INTO {table_name_safe} (video_id, publish_time)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            video_id = VALUES(video_id),
            publish_time = VALUES(publish_time)
        """
        self.execute_query_many(sql, data_list)
        print(f"[SUCCESS] Video IDs processed in {table_name}")

    def fetch_videoIds(self, table_name):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_IDS`"

        print(f"[INFO] Fetching all video IDs from {table_name}")
        sql = f"SELECT * FROM {table_name_safe} ORDER BY publish_time DESC"
        result = self.fetch_all(sql)
        print(f"[SUCCESS] Fetched all video IDs from {table_name}")
        return result
           
class MySQLYouTubeDB(VideoDataManager, VideoIdManager):
    """댓글과 비디오 데이터를 모두 관리하는 클래스"""
    pass
