from src.app.database.db_manager import MysqlSSHManager
from src.app.database.interface.video import IVideoDataManager, IVideoIdManager

class VideoDataManager(IVideoDataManager):
    """비디오 데이터를 관리하는 클래스"""
    def __init__(self, db_main: MysqlSSHManager):
        self.db_manager = db_main

    def upsert_data(self, table_name, data):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_VIDEO`"

        if isinstance(data, list):
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
                for video in data
            ]
        elif isinstance(data, dict):
            data_list = [
                (
                    data["video_id"],
                    data["title"],
                    data["view_count"],
                    data["like_count"],
                    data["comment_count"],
                    data["publish_time"],
                    data["is_shorts"],
                )
            ]
        else:
            data_list = []  # video_data가 알 수 없는 타입일 경우 빈 리스트 반환
            
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
        self.db_manager.execute_query_many(sql, data_list)
        print(f"[SUCCESS] Video data processed in {table_name}")
    
    def fetch_all(self, table_name):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_VIDEO`"
        print(f"[INFO] Fetching all video data from {table_name}")
        sql = f"SELECT * FROM {table_name_safe} ORDER BY publish_time DESC"
        result = self.db_manager.fetch_all(sql)
        print(f"[SUCCESS] Fetched all video data from {table_name}")
        return result
    
class VideoIdManager(IVideoIdManager):
    """비디오 아이디를 관리하는 클래스"""
    def __init__(self, db_main: MysqlSSHManager):
        self.db_manager = db_main
    
    def upsert_data(self, table_name, data):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_IDS`"
        print(f"[INFO] Inserting or updating video IDs in {table_name}:")
        data_list = [
            (
                video_id["video_id"],
                video_id["publish_time"]
            )
            for video_id in data
        ]
        sql = f"""
        INSERT INTO {table_name_safe} (video_id, publish_time)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            video_id = VALUES(video_id),
            publish_time = VALUES(publish_time)
        """
        self.db_manager.execute_query_many(sql, data_list)
        print(f"[SUCCESS] Video IDs processed in {table_name}")

    def fetch_all(self, table_name):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_IDS`"

        print(f"[INFO] Fetching all video IDs from {table_name}")
        sql = f"SELECT * FROM {table_name_safe} ORDER BY publish_time DESC"
        result = self.db_manager.fetch_all(sql)
        print(f"[SUCCESS] Fetched all video IDs from {table_name}")
        return result