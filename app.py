from flask import Flask, render_template, jsonify, Blueprint, request
import os, json
from scripts.youtube import YouTubeManager
from scripts.html_genertator import HTMLGenerator
from DB.database import MySQLYouTubeDB
from config.api_config import api_key

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

# Flask app initialization
app = Flask(__name__, static_folder='static', template_folder='templates')

# Register Blueprint for comments
app.register_blueprint(comments_bp)

@app.route('/')
def index():
    db_manager = MySQLYouTubeDB()  # Initialize database manager
    db_manager.connect()
    youtube_creator = YOUTUBECreatorWebsite(
        channelID="UCW945UjEs6Jm3rVNvPEALdg",
        api_key=api_key[0]
    )
    youtube_creator.update_index_html(
        index_path="templates/index.html",
        db_manager=db_manager,
        update_video_ids=True
    )
    db_manager.close()
    return render_template('index.html')  # Renders the updated index.html

@app.route('/LinkData', methods=['GET'])
def get_LinkData():
    JSON_FILE_PATH = os.path.join(os.getcwd(), 'json', 'LinkData.json')
    try:
        # Read JSON file
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
        # Read JSON file
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
    app.run(debug=True)
