from flask import jsonify, Blueprint, request
from scripts.youtube_website import YOUTUBECreatorWebsite
from config.api_config import get_api_key

# Define Blueprints for each channel
comments_bp_1 = Blueprint('friendshiping_comments', __name__, url_prefix='/friendshiping')
comments_bp_2 = Blueprint('suhyeon_comments', __name__, url_prefix='/suhyeon')
comments_bp_3 = Blueprint('bokyem_comments', __name__, url_prefix='/bokyem')
comments_bp_4 = Blueprint('loveme_comments', __name__, url_prefix='/loveme')
comments_bp_5 = Blueprint('cat_comments', __name__, url_prefix='/cat')

def get_comments(channel_name, video_id):
    """Fetch comments for a specific video."""
    if not video_id:
        return jsonify({'error': 'videoId is missing'}), 400

    try:
        youtube_creator = YOUTUBECreatorWebsite(
            api_key=get_api_key(6),
            channelName=channel_name
        )
        comments = youtube_creator.youtube_manager.api_manager.get_comments(video_id=video_id)
        return jsonify(comments)  # Return comments in JSON format
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500

# Define routes using the common `get_comments` function
@comments_bp_1.route('/comments', methods=['GET'])
def get_friendshiping_comments():
    video_id = request.args.get('videoId')
    return get_comments("우정잉", video_id)

@comments_bp_2.route('/comments', methods=['GET'])
def get_suhyeon_comments():
    video_id = request.args.get('videoId')
    return get_comments("유수현", video_id)

@comments_bp_3.route('/comments', methods=['GET'])
def get_bokyem_comments():
    video_id = request.args.get('videoId')
    return get_comments("보겸", video_id)

@comments_bp_4.route('/comments', methods=['GET'])
def get_loveme_comments():
    video_id = request.args.get('videoId')
    return get_comments("김럽미", video_id)

@comments_bp_5.route('/comments', methods=['GET'])
def get_cat_comments():
    video_id = request.args.get('videoId')
    return get_comments("지식줄고양", video_id)

