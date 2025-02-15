import pymysql

SSH_HOST = "ssh.pythonanywhere.com"
SSH_USER = "ytbCreator"
SSH_PASSWORD = "junhee2483"  # SSH 비밀번호
MYSQL_HOST = "ytbCreator.mysql.pythonanywhere-services.com"
MYSQL_USER = "ytbCreator"
MYSQL_PASSWORD = "p0890890"  # MySQL 비밀번호
MYSQL_DATABASE= "ytbCreator$YoutubeDATA1"

DB_CONFIG_DEFAULT = {
    'host': MYSQL_HOST,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database':MYSQL_DATABASE,
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
    'database':MYSQL_DATABASE,
    'cursorclass': pymysql.cursors.DictCursor,
    "connect_timeout": 10,  # MySQL 연결 타임아웃
    "read_timeout" : 10,     # 읽기 타임아웃 설정
    "autocommit" : False,      # 자동 커밋 설정
    "ssl": None  # SSL 비활성화
}

