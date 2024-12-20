import mysql.connector
import json
from datetime import datetime  

class DatabaseManager:
    def __init__(self, host, user, password, database):
        """데이터베이스 연결 초기화"""
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def insert_comments(self, video_id, author, text, like_count):
        """진행 상황 로그를 삽입"""
        sql = """
        INSERT INTO comments (video_id, author, text, like_count)
        VALUES (%s, %s, %s, %s)
        """
        values = (video_id, author, text, like_count)

        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"[comments] Inserted: {video_id} - {author}")
        except Exception as e:
            print(f"[Error] Failed to insert comments: {e}")

    def insert_videoId(self, video_id):
        """진행 상황 로그를 삽입"""
        sql = """
        INSERT INTO videoId (video_id)
        VALUES (%s)
        """
        values = (video_id, )
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"[videoId] Inserted: {video_id}")
        except Exception as e:
            print(f"[Error] Failed to insert videoId: {e}")

    def insert_videodata(self, video_id, title, view_count, like_count, comment_count, publish_time, is_shorts):
        sql = """
        INSERT INTO videoData (video_id, title, view_count, like_count, comment_count, publish_time, is_shorts)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (video_id, title, view_count, like_count, comment_count, publish_time, is_shorts)
        try:
            self.cursor.execute(sql, values)
            self.conn.commit()
            print(f"[VideoData] Inserted: {video_id} - {title}")
        except Exception as e:
            print(f"[Error] Failed to insert video data: {e}")
            
    def close(self):
        """데이터베이스 연결 종료"""
        self.cursor.close()
        self.conn.close()

def read_json_and_insert(json_file, db_handler: DatabaseManager):
    try:
        if json_file=="vidoes_data.json":
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                for entry in data:
                    video_id = entry['video_id']
                    title = entry['title']
                    view_count = entry['view_count']
                    like_count = entry['like_count']
                    comment_count = entry['comment_count']
                    publish_time = datetime.strptime(
                        entry['publish_time'], 
                        "%Y-%m-%dT%H:%M:%SZ"
                        )
                    is_shorts = entry['is_shorts']
                    
                    db_handler.insert_videodata(
                        video_id, title, view_count, like_count, comment_count, publish_time, is_shorts
                    )
        if json_file=="videoId.json":
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                for entry in data:            
                    db_handler.insert_videoId(video_id=entry)
        if json_file=="comments_data.json":
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
                for video_id, comments in data.items():
                    for comment in comments:
                        author = comment['author']
                        text = comment['text']
                        like_count = comment['like_count']
                        
                        db_handler.insert_comments(video_id, author, text, like_count)
    except Exception as e:
        print(f"[Error] Failed to read JSON or insert data: {e}")

if __name__=="__main__":
    db_config = {"host": "localhost", "user": "youtube", 
                    "password": "2483", "database": "youtubeDATA"}

    database_manager = DatabaseManager(**db_config)
    
    # json_file="comments_data.json"
    # read_json_and_insert(json_file, database_manager)
    json_file="vidoes_data.json"
    read_json_and_insert(json_file, database_manager)
    # json_file="videoId.json"
    # read_json_and_insert(json_file, database_manager)
    
    