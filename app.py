import logging, os
from flask import Flask, render_template, jsonify, g
from config.api_config import get_api_key
from routes.comments import comments_bp
from routes.link_routes import links_bp
from modules.database import MySQLYouTubeDB
from modules.Youtube import YOUTUBECreatorWebsite
from modules.Youtube import save_main_index_to_file

# Flask 애플리케이션 생성
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Register Blueprint for comments
app.register_blueprint(comments_bp)
app.register_blueprint(links_bp)

# 전역 변수로 DB 매니저 초기화
db_manager = None

# 로깅 설정
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 데이터베이스 초기화
def initialize_db_manager():
    """DB 매니저 초기화"""
    global db_manager
    try:
        db_manager = MySQLYouTubeDB()
        db_manager.connect()
        app.logger.info("Database connection initialized.")
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {e}")
        raise RuntimeError("Database initialization failed.")

# YouTube 크리에이터 초기화
def initialize_youtube_creators():
    """YouTube 크리에이터 객체 초기화"""
    try:
        if not hasattr(g, 'youtube_creators'):
            g.youtube_creators = {
                "friendshiping": {
                    "creator": YOUTUBECreatorWebsite(
                        channelName="우정잉",
                        api_key=get_api_key(1)
                    ),
                    "json": {
                        "info": "우정잉_ChannelInfo.json",
                        "link": "우정잉_LinkData.json"
                    },
                    "html": "friendshiping.html"
                },
                "suhyeon": {
                    "creator": YOUTUBECreatorWebsite(
                        channelName="청산유수현 SUHYEON",
                        api_key=get_api_key(2)
                    ),
                    "json": {
                        "info": "유수현_ChannelInfo.json",
                        "link": "유수현_LinkData.json"
                    },
                    "html": "suhyeon.html"
                },
                "bokyem": {
                    "creator": YOUTUBECreatorWebsite(
                        channelName="보겸TV",
                        api_key=get_api_key(3)
                    ),
                    "json": {
                        "info": "보겸_ChannelInfo.json",
                        "link": "보겸_LinkData.json"
                    },
                    "html": "bokyem.html"
                },
                "loveme": {
                    "creator": YOUTUBECreatorWebsite(
                        channelName="김 럽미",
                        api_key=get_api_key(4)
                    ),
                    "json": {
                        "info": "김럽미_ChannelInfo.json",
                        "link": "김럽미_LinkData.json"
                    },
                    "html": "loveme.html"
                },
                "cat": {
                    "creator": YOUTUBECreatorWebsite(
                        channelName="지식줄고양",
                        api_key=get_api_key(5)
                    ),
                    "json": {
                        "info": "지식줄고양_ChannelInfo.json",
                        "link": "지식줄고양_LinkData.json"
                    },
                    "html": "cat.html"
                }
            }
            app.logger.info("YouTube creators initialized successfully.")
    except Exception as e:
        app.logger.error(f"Error initializing YouTube creators: {e}")
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
        app.logger.info("Database connection closed.")

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
        json_path = os.path.join('./json', creator_data["json"]["info"])
        output_path = os.path.join('templates', creator_data["html"])

        # HTML 업데이트
        creator.update_index_html(
            index_path=output_path,
            db_manager=g.db_manager,
            update_video_ids=True
        )
        return render_template(creator_data["html"])
    except Exception as e:
        app.logger.error(f"Error rendering channel {channel_name}: {e}")
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
    initialize_db_manager()  # 애플리케이션 시작 시 데이터베이스 초기화
    return app

# WSGI 인터페이스를 위한 앱 객체
application = create_app()
