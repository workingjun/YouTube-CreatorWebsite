from src.app.database.mysql_manager import BaseDatabaseManager

class LinksManager(BaseDatabaseManager):
    """비디오 아이디를 관리하는 클래스"""
    
    def upsert_friendshiping_Links(self, video_data_list):
        self.upsert_Links("우정잉", video_data_list)
    
    def upsert_suhyeon_Links(self, video_data_list):
        self.upsert_Links("청산유수현 SUHYEON", video_data_list)

    def upsert_bokyem_Links(self, video_data_list):
        self.upsert_Links("보겸TV", video_data_list)

    def upsert_loveme_Links(self, video_data_list):
        self.upsert_Links("김 럽미", video_data_list)

    def upsert_cat_Links(self, video_data_list):
        self.upsert_Links("지식줄고양", video_data_list)
    
    def fetch_all_friendshiping_Links(self):
        return self.fetch_Links("우정잉")
    
    def fetch_all_suhyeon_Links(self):
        return self.fetch_Links("청산유수현 SUHYEON")
    
    def fetch_all_bokyem_Links(self):
        return self.fetch_Links("보겸TV")
    
    def fetch_all_loveme_Links(self):
        return self.fetch_Links("김 럽미")
    
    def fetch_all_cat_Links(self):
        return self.fetch_Links("지식줄고양")
    
    def upsert_Links(self, table_name, links_list):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_Links`"
        print(f"[INFO] Inserting or updating links in {table_name}:")
        
        data_list = [
            (
                link["name"],
                link["image_link"],
                link["external_link"]
            )
            for link in links_list
        ]
        sql = f"""
        INSERT INTO {table_name_safe} (name, image_link, external_link)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            image_link = VALUES(image_link),
            external_link = VALUES(external_link)
        """
        self.execute_query_many(sql, data_list)
        print(f"[SUCCESS] Links processed in {table_name}")

    def fetch_Links(self, table_name):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_Links`"

        print(f"[INFO] Fetching all links from {table_name}")
        sql = f"SELECT * FROM {table_name_safe} ORDER BY id ASC"
        result = self.fetch_all(sql)
        print(f"[SUCCESS] Fetched all links from {table_name}")

        return result