from config.api_config import get_api_key
from flask import jsonify, Blueprint, request
from modules.youtube.youtube_website import YOUTUBECreatorWebsite

# Define a single Blueprint for comments
comments_bp = Blueprint('comments', __name__, url_prefix='/<channel_name>')

# 채널별 API 키 매핑 (예시)
CHANNEL_API_KEYS = {
    "friendshiping": 1,
    "suhyeon": 2,
    "bokyem": 3,
    "loveme": 4,
    "cat": 5,
}

# 채널 이름 매핑
CHANNEL_NAMES = {
    "friendshiping": "우정잉",
    "suhyeon": "유수현",
    "bokyem": "보겸",
    "loveme": "김럽미",
    "cat": "지식줄고양",
}

def get_comments(channel_name, video_id, api_key_index):
    """Fetch comments for a specific video."""
    if not video_id:
        return jsonify({'error': 'videoId is missing'}), 400

    try:
        youtube_creator = YOUTUBECreatorWebsite(
            api_key=get_api_key(api_key_index),
            channelName=channel_name
        )
        comments = youtube_creator.youtube_manager.api_manager.get_comments(video_id=video_id)
        return jsonify(comments)  # Return comments in JSON format
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500

# Define a dynamic route for comments
@comments_bp.route('/comments', methods=['GET'])
def get_channel_comments(channel_name):
    """Fetch comments dynamically based on the channel name."""
    video_id = request.args.get('videoId')
    if channel_name not in CHANNEL_API_KEYS or channel_name not in CHANNEL_NAMES:
        return jsonify({'error': 'Invalid channel name'}), 404

    # Get the API key index and channel name
    api_key_index = CHANNEL_API_KEYS[channel_name]
    channel_full_name = CHANNEL_NAMES[channel_name]

    return get_comments(channel_full_name, video_id, api_key_index)

