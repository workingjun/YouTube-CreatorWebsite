import pymysql
import pymysql.cursors

SSH_HOST = "test.ssh.pythonanywhere.com"
SSH_USER = "testUser"
SSH_PASSWORD = "testPassword"
MYSQL_HOST = "test.mysql.pythonanywhere-services.com"
MYSQL_USER = "testUser"
MYSQL_PASSWORD = "testDBPassword"
MYSQL_DB = "testDatabase"

DB_CONFIG_DEFAULT = {
    'host': MYSQL_HOST,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DB,
    'cursorclass': pymysql.cursors.DictCursor,
    "connect_timeout": 10,  # MySQL 연결 타임아웃
    "read_timeout" : 10,     # 읽기 타임아웃 설정
    "autocommit" : False,      # 자동 커밋 설정
    "ssl": None  # SSL 비활성화
}

DB_CONFIG_SSH = {
    'host': "127.0.0.1",
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DB,
    'cursorclass': pymysql.cursors.DictCursor,
    "connect_timeout": 10,  # MySQL 연결 타임아웃
    "read_timeout" : 10,     # 읽기 타임아웃 설정
    "autocommit" : False,      # 자동 커밋 설정
    "ssl": None  # SSL 비활성화
}