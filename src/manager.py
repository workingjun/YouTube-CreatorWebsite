import os
from flask import Flask, render_template, request, jsonify, g
from src.app.routes import comments_bp, channel_bp
## import DB 
from src.app.youtube import YOUTUBECreatorWebsite
from src.app.youtube import save_main_index_to_file
from src.utils.custom_logging import GetLogger
from src.utils.yamL import load_yaml, append_yaml

FILE_NAME_API = './config/api_config.dev.yaml'
FILE_NAME_DB = './config/db_config.dev.yaml'

# Flask 애플리케이션 생성
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Register Blueprint for comments
app.register_blueprint(comments_bp)
app.register_blueprint(channel_bp)

# 전역 변수로 DB 매니저 초기화
db_manager = None
logger = None
g.youtube_creators = {}

API_KEY = load_yaml(FILE_NAME_API)
DB_CONFIG = load_yaml(FILE_NAME_DB)["default"]

def initialize_db_manager():
    """요청 전에 DB 연결 및 크리에이터 초기화"""
    global db_manager
    if not db_manager:
        g.db_manager = MySQLYouTubeDBFactory(DB_CONFIG)
        g.db_manager.db_core.connect()

def initialize_youtube_creators(api_key, channel_name):
    """YouTube 크리에이터 객체 초기화"""
    try:
        # 크리에이터 객체 생성
        g.youtube_creators[channel_name] = {
            "creator": YOUTUBECreatorWebsite(
                api_key=api_key,
                channel_name=channel_name
            ),
            "html": f"{channel_name}.html"
        }
        print(f"Creator for {channel_name} initialized successfully.")
        logger.info("YouTube creators initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing YouTube creators: {e}")
        raise

# 애플리케이션 메인 페이지
@app.route('/', methods=["GET"])
def index():
    """메인 페이지 렌더링"""
    channel_name = request.args.get("channel_name")
    initialize_youtube_creators(channel_name, API_KEY[1])
    save_main_index_to_file(db_manager)
    return render_template('main.html')

# WSGI 서버 초기화
def create_app():
    """PythonAnywhere WSGI 서버를 위한 앱 생성"""
    global logger
    logger = GetLogger(
        "logger_app", "src/logs/app.log", 
        "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
        )
    initialize_db_manager()  # 애플리케이션 시작 시 데이터베이스 초기화
    return app

# WSGI 인터페이스를 위한 앱 객체
application = create_app()