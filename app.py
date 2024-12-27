from flask import Flask, render_template, jsonify
from routes.comments import comments_bp
import os, json

app = Flask(__name__, static_folder='statics', template_folder='template')
app.register_blueprint(comments_bp)

@app.route('/')
def index():
    return render_template('index.html')  # template/index.html 렌더링

@app.route('/links', methods=['GET'])
def get_links():
    try:
        JSON_FILE_PATH = os.path.join(os.getcwd(), 'transfer_files/json', 'link_data.json')
        # JSON 파일 읽기
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return jsonify(data)  # JSON 데이터를 반환
    except FileNotFoundError:
        return jsonify({"error": "JSON 파일을 찾을 수 없습니다."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "JSON 파일의 형식이 올바르지 않습니다."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()