from src.app.database.mysql_manager import BaseDatabaseManager

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
    
    def upsert_videoData(self, table_name, video_data):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_VIDEO`"

        if isinstance(video_data, list):
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
                for video in video_data
            ]
        elif isinstance(video_data, dict):
            data_list = [
                (
                    video_data["video_id"],
                    video_data["title"],
                    video_data["view_count"],
                    video_data["like_count"],
                    video_data["comment_count"],
                    video_data["publish_time"],
                    video_data["is_shorts"],
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