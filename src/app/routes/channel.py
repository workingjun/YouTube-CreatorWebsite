import os
from flask import jsonify, Blueprint, request
from flask import Flask, render_template, request, jsonify, g
from src.app.youtube.ytb_creator_website import YOUTUBECreatorWebsite

channel_bp = Blueprint('comments', __name__, url_prefix='/<channel_name>')

# 채널 데이터 렌더링
@channel_bp.route('/<channel_name>')
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
        print(f"Error rendering channel {channel_name}: {e}")
        return jsonify({"error": str(e)}), 500