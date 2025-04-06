from src.app.database.db_manager import MysqlSSHManager

class LinksManager:
    """비디오 아이디를 관리하는 클래스"""
    def __init__(self, db_main: MysqlSSHManager):
        self.db_manager = db_main

    def execute_query_many(self, table_name, links_list):
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
        self.db_manager.execute_query_many(sql, data_list)
        print(f"[SUCCESS] Links processed in {table_name}")

    def fetch_all(self, table_name):
        # 테이블 이름을 백틱으로 감싸기
        table_name_safe = f"`{table_name}_Links`"

        print(f"[INFO] Fetching all links from {table_name}")
        sql = f"SELECT * FROM {table_name_safe} ORDER BY id ASC"
        result = self.db_manager.fetch_all(sql)
        print(f"[SUCCESS] Fetched all links from {table_name}")

        return result