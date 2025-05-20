import os, yaml

def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
    
def append_yaml(filename, append_data):
    # 기존 데이터 불러오기
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}

    data.setdefault('videos', []).append(append_data)

    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)