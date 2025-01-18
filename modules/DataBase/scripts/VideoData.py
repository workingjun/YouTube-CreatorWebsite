from modules.database.scripts.mysql_ssh_manager import BaseDatabaseManager

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