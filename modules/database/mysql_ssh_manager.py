import pymysql, time
from config.db_config import DB_CONFIG_SSH
from config.db_config import DB_CONFIG_DEFAULT
from modules.database.ssh_tunnel import start_ssh_tunnel
from modules.database.ssh_tunnel import stop_ssh_tunnel

class BaseDatabaseManager:
    def __init__(self):
        self._shared_connection = None

    def connect(self, ssh_flags: bool=False, retries: int=5, delay: int=5):
        if ssh_flags:
            print("[INFO] Starting SSH tunnel...")
            self._tunnel = start_ssh_tunnel()
            DB_CONFIG_SSH["port"] = self._tunnel.local_bind_port
            DB_COMFIG = DB_CONFIG_SSH
            print(f"[INFO] SSH tunnel started at local port {self._tunnel.local_bind_port}")
        else:
            DB_COMFIG = DB_CONFIG_DEFAULT

        attempt = 0
        while attempt < retries:
            try:
                if self._shared_connection is None:
                    print(f"[INFO] Attempting MySQL connection, attempt {attempt + 1} of {retries}")
                    self._shared_connection = pymysql.connect(**DB_COMFIG)

                self.conn = self._shared_connection
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
            
            except KeyboardInterrupt:
                raise

    def close(self):
        """데이터베이스 연결 종료 (공유 연결 닫기)"""
        if self._shared_connection:
            self._shared_connection.close()
            self._shared_connection = None
        stop_ssh_tunnel()

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
            self.connect(ssh_flags=True if self._tunnel else False)