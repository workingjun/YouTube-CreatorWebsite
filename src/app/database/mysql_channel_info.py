from src.app.database.mysql_manager import BaseDatabaseManager

class ChannelInfoManager(BaseDatabaseManager):
    def upsert_channel_info(self, data):
        print("[INFO] Inserting or updating channelInfo in youtube_channels:")
        
        params = (
            data["title"],
            data["channel_id"],
            data["thumbnail"],
            data["description"],
            data["subscriber_count"],
            data["video_count"],
            data["views_count"],
        )
        
        # Prepare SQL query for upsert
        sql = """
        INSERT INTO youtube_channels (title, channel_id, thumbnail, description, subscriber_count, video_count, views_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            title = VALUES(title),
            thumbnail = VALUES(thumbnail),
            description = VALUES(description),
            subscriber_count = VALUES(subscriber_count),
            video_count = VALUES(video_count),
            views_count = VALUES(views_count)
        """
        self.execute_query(sql, params)
        print("[SUCCESS] channelInfo processed in youtube_channels")
    
    def fetch_channel_info(self, title):
        
        print(f"[INFO] Fetching channelInfo for title: {title}")
        sql = "SELECT * FROM youtube_channels WHERE title = %s"

        result = self.fetch_one(sql, (title,))
        print(f"[SUCCESS] Fetched channelInfo for title: {title}")
        return result
        
    def fetch_all_channel_info(self):
        
        print("[INFO] Fetching all channelInfo")
        sql = "SELECT * FROM youtube_channels"

        result = self.fetch_all(sql)
        print("[SUCCESS] Fetched all channelInfo")
        return result