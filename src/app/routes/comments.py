from flask import jsonify, Blueprint, request
from src.config.api_config import get_api_key
from src.config.channelId import CHANNELID
from src.app.youtube.ytb_creator_website import YOUTUBECreatorWebsite

# Define a single Blueprint for comments
comments_bp = Blueprint('comments', __name__, url_prefix='/<channel_name>')

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
    if channel_name not in CHANNELID:
        return jsonify({'error': 'Invalid channel name'}), 404

    # Get the API key index and channel name
    channel_full_name = CHANNELID[channel_name]
    keys_list = list(CHANNELID.keys())  
    api_key_index = keys_list.index(channel_name)
                        
    return get_comments(channel_full_name, video_id, api_key_index)

