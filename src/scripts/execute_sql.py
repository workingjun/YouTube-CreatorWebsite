import pymysql
from src.utils.yamL import load_yaml

CHANNELINAME = load_yaml("./config/channel_name.dev.yaml")
CHANNELID = load_yaml("./config/channel_id.dev.yaml")
DB_CONFIG = load_yaml("./config/db_config.dev.yaml")["Default"]

with open('./mysql_config.txt', 'r', encoding='utf-8') as f:
    contents = f.readlines()[5:]

conn = pymysql.connect(
    charset='utf8mb4',
    **DB_CONFIG
)

try:
    with conn.cursor() as cursor:
        for name in CHANNELINAME:
            sql_statements = ''.join(contents).replace('YoutuberName', name)
            cursor.execute(sql_statements)
    conn.commit()
finally:
    conn.close()