from flask import Flask

app = Flask(__name__)  # 'statics' 폴더를 정적 파일 폴더로 설정

@app.route('/')
def index():
    return 'Test Page'

if __name__ == '__main__':
    print("Static folder path:", app.static_folder)
    app.run(debug=True)
