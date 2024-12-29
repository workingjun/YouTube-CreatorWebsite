import pymysql

SSH_HOST = "test.ssh.pythonanywhere.com"
SSH_USER = "testUser"
SSH_PASSWORD = "testPassword"
MYSQL_HOST = "test.mysql.pythonanywhere-services.com"
MYSQL_USER = "testUser"
MYSQL_PASSWORD = "testDBPassword"
MYSQL_DB = "testDatabase"

DB_CONFIG = {
    'host': MYSQL_HOST,
    'user': MYSQL_USER,
    'password': MYSQL_PASSWORD,
    'database': MYSQL_DB,
    'cursorclass': pymysql.cursors.DictCursor,
    'connect_timeout': 30,
    'ssl': None
}