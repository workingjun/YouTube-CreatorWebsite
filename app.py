from flask import Flask, render_template, jsonify, Blueprint, request, g
import os, json
from scripts.youtube import YouTubeManager
from scripts.html_genertator import HTMLGenerator
from DB.database import MySQLYouTubeDB
from config.api_config import api_key

# YouTube Creator Website class
class YOUTUBECreatorWebsite:
    def __init__(self, channelID, api_key):
        self.channelID = channelID
        self.api_key = api_key
        self.youtube_manager = YouTubeManager(api_key=self.api_key, channelID=self.channelID)
        self.html_manager = HTMLGenerator()

    def update_index_html(self, index_path, db_manager, update_video_ids:bool):
        """Updates the index.html with the latest channel data"""
        # Save channel information
        self.youtube_manager.save_channel_information()
        # Collect partial video data
        self.youtube_manager.collect_data(db_manager=db_manager, update_video_ids=update_video_ids)
        # Generate and save updated HTML file
        self.html_manager.save_index_to_file(output_path=index_path, db_manager=db_manager)
    
# Blueprint for comments functionality
comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/comments', methods=['GET'])
def get_comments():
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'videoId is missing'}), 400
    try:
        youtube_creator = YOUTUBECreatorWebsite(
            api_key=api_key[0], 
            channelID="UCW945UjEs6Jm3rVNvPEALdg"
        )
        comments = youtube_creator.youtube_manager.api_manager.get_comments(video_id=video_id)
        return jsonify(comments)  # Return comments in JSON format
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
    
app = Flask(__name__, static_folder='static', template_folder='templates')

# Register Blueprint for comments
app.register_blueprint(comments_bp)

# 전역 변수로 db_manager를 초기화
db_manager = None

# 애플리케이션 시작 시 한 번만 SSH 터널 및 DB 연결 설정
def initialize_db():
    global db_manager
    try:
        db_manager = MySQLYouTubeDB()
        db_manager.connect()
        app.logger.info("Database connection initialized.")
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {e}")
        raise RuntimeError("Database initialization failed.")

@app.before_request
def before_request():
    # 요청 중에 필요하면 전역 db_manager를 g에 설정
    if db_manager and not hasattr(g, 'db_manager'):
        g.db_manager = db_manager

@app.after_request
def after_request(response):
    # 요청이 끝난 후 별도의 동작 없음 (db_manager를 닫지 않음)
    return response

@app.teardown_appcontext
def teardown(exception):
    # 애플리케이션 종료 시 db_manager 닫기
    global db_manager
    if db_manager:
        db_manager.close()
        app.logger.info("Database connection closed.")

@app.route('/')
def index():
    if not hasattr(g, 'db_manager') or g.db_manager is None:
        try:
            g.db_manager = MySQLYouTubeDB()
            g.db_manager.connect()
        except Exception as e:
            app.logger.error(f"Database connection failed: {e}")
            return jsonify({"error": "Database connection failed"}), 500

    try:
        youtube_creator = YOUTUBECreatorWebsite(
            channelID="UCW945UjEs6Jm3rVNvPEALdg",
            api_key=api_key[0]
            )
        youtube_creator.update_index_html(
            index_path="templates/index.html",
            db_manager=g.db_manager,
            update_video_ids=True
            )
    except RuntimeError as e:
        app.logger.error(f"Failed to update index.html: {e}")
        return jsonify({"error": str(e)}), 500

    return render_template('index.html')  # Renders the updated index.html

@app.route('/LinkData', methods=['GET'])
def get_LinkData():
    JSON_FILE_PATH = os.path.join(os.getcwd(), 'json', 'LinkData.json')
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)  # Return JSON response
    except FileNotFoundError:
        return jsonify({"error": "JSON file not found."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ChannelInfo', methods=['GET'])
def get_ChannelInfo():
    JSON_FILE_PATH = os.path.join(os.getcwd(), 'json', 'ChannelInfo.json')
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)  # Return JSON response
    except FileNotFoundError:
        return jsonify({"error": "JSON file not found."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        initialize_db()  # 데이터베이스 초기화
        app.run()
    except RuntimeError as e:
        app.logger.error(e)
