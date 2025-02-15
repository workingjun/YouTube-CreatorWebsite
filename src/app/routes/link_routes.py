import json, os
from flask import Blueprint, jsonify, g

# JSON 캐싱용 딕셔너리
json_cache = {}

# JSON 데이터 로드 함수 (캐싱 사용)
def load_json_data(file_name):
    """JSON 데이터를 로드하고 캐싱"""
    if file_name not in json_cache:
        JSON_FILE_PATH = os.path.join(os.getcwd(), 'json', file_name)
        try:
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
                json_cache[file_name] = json.load(file)
        except FileNotFoundError:
            return jsonify({"error": f"{file_name} not found."}), 404
        except json.JSONDecodeError:
            return jsonify({"error": f"{file_name} has invalid JSON format."}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify(json_cache[file_name])

# 블루프린트 생성
links_bp = Blueprint('link_routes', __name__)

# 채널 JSON 데이터 반환
@links_bp.route('/<channel_name>/LinkData', methods=['GET'])
def get_link_data(channel_name):
    """채널 JSON 데이터 반환"""
    creators = getattr(g, 'youtube_creators', {})
    if channel_name not in creators:
        return jsonify({"error": "link not found"}), 404

    file_name = creators[channel_name]["json"]["link"]
    return load_json_data(file_name)

