import logging, os
from flask import Flask, render_template, jsonify, g
from src.config import get_api_key
from src.config import CHANNELID
from src.app.routes import comments_bp
from src.app.routes import links_bp
from src.app.database import MySQLYouTubeDB
from src.app.youtube import YOUTUBECreatorWebsite
from src.app.youtube import save_main_index_to_file
from src.utils.custom_logging import GetLogger

# Flask 애플리케이션 생성
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Register Blueprint for comments
app.register_blueprint(comments_bp)
app.register_blueprint(links_bp)

# 전역 변수로 DB 매니저 초기화
db_manager = None
logger = None

# 데이터베이스 초기화
def initialize_db_manager():
    """DB 매니저 초기화"""
    global db_manager
    try:
        db_manager = MySQLYouTubeDB()
        db_manager.connect()
        logger.info("Database connection initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise RuntimeError("Database initialization failed.")

def initialize_youtube_creators():
    """YouTube 크리에이터 객체 초기화"""
    try:
        if not hasattr(g, 'youtube_creators'):
            g.youtube_creators = {}

            # CHANNELID 딕셔너리의 키와 값을 enumerate와 함께 사용
            for index, (channel_name, channel_id) in enumerate(CHANNELID.items()):
                print(f"Initializing creator for channel: {channel_name} (Index: {index})")

                # API 키 가져오기
                api_key = get_api_key(index+1)
                print(f"API Key for {channel_name}: {api_key}")

                # 크리에이터 객체 생성
                g.youtube_creators[channel_name] = {
                    "creator": YOUTUBECreatorWebsite(
                        channelName=channel_name,
                        api_key=api_key
                    ),
                    "html": f"{channel_name}.html"
                }
                print(f"Creator for {channel_name} initialized successfully.")

            logger.info("YouTube creators initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing YouTube creators: {e}")
        raise

# 요청 전 작업
@app.before_request
def before_request():
    """요청 전에 DB 연결 및 크리에이터 초기화"""
    global db_manager
    if not db_manager:
        initialize_db_manager()
    g.db_manager = db_manager
    initialize_youtube_creators()

# 요청 후 작업
@app.teardown_appcontext
def teardown(exception):
    """요청 후 DB 연결 닫기"""
    if hasattr(g, 'db_manager') and g.db_manager:
        g.db_manager.close()
        logger.info("Database connection closed.")

# 채널 데이터 렌더링
@app.route('/<channel_name>')
def render_channel(channel_name):
    """동적 채널 페이지 렌더링"""
    creators = getattr(g, 'youtube_creators', {})
    if channel_name not in creators:
        return jsonify({"error": "Channel not found"}), 404

    creator_data = creators[channel_name]
    try:
        creator = creator_data["creator"]
        output_path = os.path.join('templates', creator_data["html"])

        # HTML 업데이트
        creator.update_index_html(
            index_path=output_path,
            db_manager=g.db_manager,
            update_video_ids=True
        )
        return render_template(creator_data["html"])
    except Exception as e:
        logger.error(f"Error rendering channel {channel_name}: {e}")
        return jsonify({"error": str(e)}), 500

# 애플리케이션 메인 페이지
@app.route('/')
def index():
    """메인 페이지 렌더링"""
    save_main_index_to_file(db_manager)
    return render_template('main.html')

# WSGI 서버 초기화
def create_app():
    """PythonAnywhere WSGI 서버를 위한 앱 생성"""
    global logger
    logger = GetLogger()
    initialize_db_manager()  # 애플리케이션 시작 시 데이터베이스 초기화
    return app

# WSGI 인터페이스를 위한 앱 객체
application = create_app()