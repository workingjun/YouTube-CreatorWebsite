from flask import Blueprint, request, jsonify
from DB.DataBase import DatabaseManager

db_manager = DatabaseManager()
comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/comments', methods=['GET'])
def get_comments():
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'videoId is missing'}), 400
    try:
        comments = db_manager.fetch_comments(video_id)
        return jsonify(comments)
    except RuntimeError as e:
        return jsonify({'error': str(e)}), 500
