from flask import Flask, render_template, jsonify, g
import os, json, logging
from DB.database import MySQLYouTubeDB
from config.api_config import get_api_key
from config.channelid_config import CHANNELID
from routes.comments import comments_bp_1, comments_bp_2, comments_bp_3, comments_bp_4, comments_bp_5
from scripts.youtube_website import YOUTUBECreatorWebsite
    
app = Flask(__name__, static_folder='static', template_folder='templates')

# Register Blueprint for comments
app.register_blueprint(comments_bp_1)
app.register_blueprint(comments_bp_2)
app.register_blueprint(comments_bp_3)
app.register_blueprint(comments_bp_4)
app.register_blueprint(comments_bp_5)

# 전역 변수로 db_manager를 초기화
db_manager = None

def load_json_data(file_name):
    """Load JSON data from the specified file."""
    JSON_FILE_PATH = os.path.join(os.getcwd(), 'json', file_name)
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)  # Return JSON response
    except FileNotFoundError:
        return jsonify({"error": f"{file_name} not found."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": f"{file_name} has invalid JSON format."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# 애플리케이션 시작 시 두 개의 데이터베이스 연결 설정
def initialize_db_manager(ssh_flags=False):
    global db_manager
    try:
        # 첫 번째 데이터베이스 연결
        db_manager = MySQLYouTubeDB()
        db_manager.connect(ssh_flags=ssh_flags)
        app.logger.info("Database connection initialized.")
    except Exception as e:
        app.logger.error(f"Failed to initialize one or more databases: {e}")
        raise RuntimeError("Database initialization failed.")

def render_channel_page(creator_variable, output_path, json_path):
    try:
        # Update the HTML with fresh data
        youtube_creator = getattr(g, creator_variable, None)
        if not youtube_creator:
            raise RuntimeError(f"Channel {creator_variable} not initialized in request context.")
        
        youtube_creator.update_index_html(
            index_path=output_path,
            db_manager=g.db_manager,
            update_video_ids=True,
            ChannelInfo_filepath=json_path
        )
        html_template = output_path.split("/")[-1]
        return render_template(html_template)  # Render updated template
    except RuntimeError as e:
        logging.error(f"Failed to update {html_template}: {e}")
        return jsonify({"error": str(e)}), 500

def initialize_youtube_creators(app):
    """
    Initialize YouTube creator objects in the Flask request context (g).
    """
    try:
        if not hasattr(g, 'youtube_creator_1'):
            g.youtube_creator_1 = YOUTUBECreatorWebsite(
                channelName="우정잉",
                api_key=get_api_key(1)
            )
            app.logger.info("youtube_creator_1 initialized successfully.")

        if not hasattr(g, 'youtube_creator_2'):
            g.youtube_creator_2 = YOUTUBECreatorWebsite(
                channelName="유수현",
                api_key=get_api_key(2)
            )
            app.logger.info("youtube_creator_2 initialized successfully.")

        if not hasattr(g, 'youtube_creator_3'):
            g.youtube_creator_3 = YOUTUBECreatorWebsite(
                channelName="보겸",
                api_key=get_api_key(3)
            )
            app.logger.info("youtube_creator_3 initialized successfully.")

        if not hasattr(g, 'youtube_creator_4'):
            g.youtube_creator_4 = YOUTUBECreatorWebsite(
                channelName="김럽미",
                api_key=get_api_key(4)
            )
            app.logger.info("youtube_creator_4 initialized successfully.")

        if not hasattr(g, 'youtube_creator_5'):
            g.youtube_creator_5 = YOUTUBECreatorWebsite(
                channelName="지식줄고양",
                api_key=get_api_key(5)
            )
            app.logger.info("youtube_creator_5 initialized successfully.")
    except Exception as e:
        app.logger.error(f"Error initializing YouTube creators: {e}")
        raise


@app.before_request
def before_request():
    """Set up database connections and other per-request resources."""
    global db_manager

    if not db_manager:
        # Initialize db_manager
        initialize_db_manager(ssh_flags=False)
    g.db_manager = db_manager
    app.logger.info("db_manager is properly initialized.")

    # Initialize YouTube creators
    try:
        initialize_youtube_creators(app)
        app.logger.info("YouTube creators initialized successfully.")
    except Exception as e:
        app.logger.error(f"Failed to initialize YouTube creators: {e}")
        return jsonify({"error": "Failed to initialize YouTube creators."}), 500


@app.teardown_appcontext
def teardown(exception):
    """Close database connections at the end of the app context."""
    db_manager = getattr(g, 'db_manager', None)
    if db_manager:
        db_manager.close()
        app.logger.info("Database connection closed.")

@app.route('/')
def index():
    return render_template('main.html')  # Render updated template
    
@app.route('/friendshiping')
def friendshiping():
    """Render the friendshiping.html with updated data."""
    return render_channel_page(
        creator_variable="youtube_creator_1",
        output_path="templates/friendshiping.html",
        json_path="./json/우정잉_ChannelInfo.json"
    )

@app.route('/suhyeon')
def suhyeon():
    """Render the suhyeon.html with updated data."""
    return render_channel_page(
        creator_variable="youtube_creator_2",
        output_path="templates/suhyeon.html",
        json_path="./json/유수현_ChannelInfo.json"
    )

@app.route('/bokyem')
def bokyem():
    """Render the suhyeon.html with updated data."""
    return render_channel_page(
        creator_variable="youtube_creator_3",
        output_path="templates/bokyem.html",
        json_path="./json/보겸_ChannelInfo.json"
    )

@app.route('/loveme')
def loveme():
    """Render the suhyeon.html with updated data."""
    return render_channel_page(
        creator_variable="youtube_creator_4",
        output_path="templates/loveme.html",
        json_path="./json/김럽미_ChannelInfo.json"
    )

@app.route('/cat')
def cat():
    """Render the suhyeon.html with updated data."""
    return render_channel_page(
        creator_variable="youtube_creator_5",
        output_path="templates/cat.html",
        json_path="./json/지식줄고양_ChannelInfo.json"
    )

@app.route('/friendshiping/ChannelInfo', methods=['GET'])
def get_friendshiping_channel_info():
    return load_json_data('우정잉_ChannelInfo.json')

@app.route('/suhyeon/ChannelInfo', methods=['GET'])
def get_suhyeon_channel_info():
    return load_json_data('유수현_ChannelInfo.json')

@app.route('/bokyem/ChannelInfo', methods=['GET'])
def get_bokyem_channel_info():
    return load_json_data('보겸_ChannelInfo.json')

@app.route('/loveme/ChannelInfo', methods=['GET'])
def get_loveme_channel_info():
    return load_json_data('김럽미_ChannelInfo.json')

@app.route('/cat/ChannelInfo', methods=['GET'])
def get_cat_channel_info():
    return load_json_data('지식줄고양_ChannelInfo.json')

@app.route('/friendshiping/LinkData', methods=['GET'])
def get_friendshiping_link_data():
    return load_json_data('우정잉_LinkData.json')

@app.route('/suhyeon/LinkData', methods=['GET'])
def get_suhyeon_link_data():
    return load_json_data('유수현_LinkData.json')

@app.route('/bokyem/LinkData', methods=['GET'])
def get_bokyem_link_data():
    return load_json_data('보겸_LinkData.json')

@app.route('/loveme/LinkData', methods=['GET'])
def get_loveme_link_data():
    return load_json_data('김럽미_LinkData.json')

@app.route('/cat/LinkData', methods=['GET'])
def get_cat_link_data():
    return load_json_data('지식줄고양_LinkData.json')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except RuntimeError as e:
        app.logger.error(e)
