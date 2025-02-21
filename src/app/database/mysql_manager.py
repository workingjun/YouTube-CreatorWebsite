import pymysql, time
from ssh_tunnel import start_ssh_tunnel
from ssh_tunnel import stop_ssh_tunnel

class BaseDatabaseManager:
    _instance = None
    _tunnel = None
    _conn = None
    ssh_flags: bool
    DB_CONFIG: dict

    def __new__(cls, DB_CONFIG, ssh_flags: bool = False):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.ssh_flags = ssh_flags  # 인스턴스 변수로 저장
            cls._instance.DB_CONFIG = DB_CONFIG  # 인스턴스 변수로 저장
            cls._instance.connect()
        return cls._instance

    def connect(self, retries: int=5, delay: int=5):
        if self._conn is not None:  # 기존 연결이 있으면 새로 연결하지 않음
            print("[INFO] Using existing MySQL connection.")
            return
        
        if self.ssh_flags:
            print("[INFO] Starting SSH tunnel...")
            self._tunnel = start_ssh_tunnel()
            self.DB_CONFIG["port"] = self._tunnel.local_bind_port
            print(f"[INFO] SSH tunnel started at local port {self._tunnel.local_bind_port}")

        attempt = 0
        while attempt < retries:
            try:
                print(f"[INFO] Attempting MySQL connection, attempt {attempt + 1} of {retries}")
                self._conn = pymysql.connect(**self.DB_CONFIG)
                self.cursor = self._conn.cursor()
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
        if self._conn:
            self._conn.close()
            self._conn = None
        if self._tunnel:
            stop_ssh_tunnel()

    def execute_query(self, query, values=None):
        try:
            self.ensure_connection()
            self.cursor.execute(query, values)
            self._conn.commit()
            print("[SUCCESS] Batch query executed.")
        except Exception as e:
            self._conn.rollback()  # Rollback the transaction in case of an error
            print(f"[ERROR] Batch query failed: {e}")

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
            self._conn.commit()  # Commit the transaction
            print("[SUCCESS] Batch query executed.")
        except Exception as e:
            self._conn.rollback()  # Rollback the transaction in case of an error
            print(f"[ERROR] Batch query failed: {e}")

    def ensure_connection(self):
        """MySQL 연결이 유효한지 확인하고, 끊어진 경우 재연결"""
        try:
            # MySQL 연결 상태 확인 (reconnect=True 옵션으로 끊어진 경우 복구)
            self._conn.ping(reconnect=True)
        except pymysql.MySQLError as e:
            print("[ERROR] Connection lost. Reconnecting...")
            # 끊어진 경우 재연결 수행
            self.connect()

