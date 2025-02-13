from modules.database.mysql_ssh_manager import BaseDatabaseManager

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