import pymysql, time
from src.app.database.ssh_tunnel import start_ssh_tunnel, stop_ssh_tunnel
from src.utils.custom_logging import GetLogger, CustomLogging

class BaseDatabaseManager:
    _instance = None
    _tunnel = None
    _conn = None
    logger: CustomLogging
    ssh_flags: bool
    DB_CONFIG: dict

    def __new__(cls, DB_CONFIG, ssh_flags: bool = False):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.ssh_flags = ssh_flags
            cls._instance.DB_CONFIG = DB_CONFIG
            cls._instance.logger = GetLogger("logger_db", "src/logs/db_manager.log",
                                             "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")
            cls._instance.connect()
        return cls._instance

    def connect(self, retries: int = 5, delay: int = 5):
        if self._conn is not None:
            self.logger.info("Using existing MySQL connection.")
            return

        if self.ssh_flags:
            self.logger.info("Starting SSH tunnel...")
            self._tunnel = start_ssh_tunnel()
            self.DB_CONFIG["port"] = self._tunnel.local_bind_port
            self.logger.info("SSH tunnel started at local port %s", self._tunnel.local_bind_port)

        attempt = 0
        while attempt < retries:
            try:
                self.logger.info("Attempting MySQL connection, attempt %s of %s", attempt + 1, retries)
                self._conn = pymysql.connect(**self.DB_CONFIG)
                self.logger.info("MySQL connection established")
                self.ensure_connection()
                return
            except pymysql.MySQLError as e:
                self.logger.error("MySQL connection failed: %s", str(e))
                attempt += 1
                if attempt < retries:
                    self.logger.info("Retrying in %s seconds...", delay)
                    time.sleep(delay)
                else:
                    raise Exception(f"Failed to connect to MySQL after {retries} attempts.")
            except KeyboardInterrupt:
                raise

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            self.logger.info("MySQL connection closed.")

        if self._tunnel is not None:
            self.logger.info("Stopping SSH tunnel...")
            stop_ssh_tunnel()
            self._tunnel = None

    def fetch_all(self, query, values=None):
        try:
            self.ensure_connection()
            with self._conn.cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchall()
                if not result:
                    self.logger.warning("Query returned empty result set. Query: %s, Values: %s", query, values or "None")
                return result
        except pymysql.MySQLError as e:
            self.logger.error("Fetching data failed. Query: %s, Values: %s, Error: %s", query, values or "None", str(e))
            return []

    def fetch_one(self, query, values=None):
        try:
            self.ensure_connection()
            with self._conn.cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
                if result is None:
                    self.logger.warning("Query returned no results. Query: %s, Values: %s", query, values or "None")
                return result
        except pymysql.MySQLError as e:
            self.logger.error("Fetching data failed. Query: %s, Values: %s, Error: %s", query, values or "None", str(e))
            return None

    def execute_query(self, query, values=None):
        try:
            self.ensure_connection()
            with self._conn.cursor() as cursor:
                cursor.execute(query, values)
                self._conn.commit()
                self.logger.info("Query executed successfully. Query: %s, Values: %s", query, values)
        except Exception as e:
            self.logger.error("Query execution failed. Query: %s, Values: %s, Error: %s", query, values, str(e))
            self._conn.rollback()

    def execute_query_many(self, query, data_list):
        try:
            self.ensure_connection()
            with self._conn.cursor() as cursor:
                cursor.executemany(query, data_list)
                self._conn.commit()
                self.logger.info("Batch query executed successfully. Query: %s, Data: %s", query, data_list)
        except Exception as e:
            self.logger.error("Batch query execution failed. Query: %s, Data: %s, Error: %s", query, data_list, str(e))
            self._conn.rollback()

    def ensure_connection(self):
        if self._conn is None:
            self.logger.error("Connection is None. Reconnecting...")
            self.connect()
            return
        
        try:
            self._conn.ping(reconnect=True)
        except pymysql.MySQLError as e:
            self.logger.error("Connection lost. Reconnecting... Error: %s", str(e))
            self.connect()

