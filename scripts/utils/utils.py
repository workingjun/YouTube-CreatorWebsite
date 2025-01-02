import re, os, json
from datetime import datetime, timedelta

def load_template():
    with open("templates/template.html", "r", encoding="utf-8") as file:
        template = file.read()
        template = template.replace("{", "{{").replace("}", "}}")
        template = template.replace("{{channel_name}}", "{channel_name}")
        template = template.replace("{{channelID}}", "{channelID}")
        template = template.replace("{{subscriber_count}}", "{subscriber_count}")
        template = template.replace("{{video_cards}}", "{video_cards}")
        template = template.replace("{{last_video_cards}}", "{last_video_cards}")
        template = template.replace("{{thumbnail}}", "{thumbnail}")
        template = template.replace("{{subscriber_count}}", "{subscriber_count}")
        template = template.replace("{{description}}", "{description}")
        template = template.replace("{{video_count}}", "{video_count}")
        template = template.replace("{{views_count}}", "{views_count}")
        return template

def load_main():
    with open("templates/template_main.html", "r", encoding="utf-8") as file:
        template = file.read()
        template = template.replace("{", "{{").replace("}", "}}")
        template = template.replace("{{container}}", "{container}")
        return template

def save_mainindex_to_file():
    # JSON 파일이 저장된 폴더 경로
    folder_path = "json/"

    # 폴더 내 모든 JSON 파일 읽기
    json_data_list = []
    info_cards_list = []

    for filename in os.listdir(folder_path):
        if filename.endswith("ChannelInfo.json"):  # 확장자가 .json인 파일만 읽기
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)  # JSON 파일 읽기
                    json_data_list.append(data)  # 데이터를 리스트에 추가
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # 모든 JSON 데이터 출력
    for data in json_data_list:
        view_count = format(data['views_count'], ",")
        video_count = format(data['video_count'], ",")
        subscriber_count = format(data['subscriber_count'], ",")

        info_cards_list.append(f"""<div class="card">
        <img src="{data["thumbnail"]}" alt="{data["title"]}">
        <h3><a href="{get_url(data["title"])}">{data["title"]}</a></h3>
        <p>구독자 수: {subscriber_count}</p>
        <p>전체 조회 수: {view_count}</p>
        <p>등록된 영상 수: {video_count}</p>
    </div>
    """)
    main_templates = load_main()
    main_html_output = main_templates.format(
        container="".join(info_cards_list)
    )
    with open("templates/main.html", "w", encoding="utf-8") as file:
        file.write(main_html_output)

def get_url(text):
    if "우정잉" in text:
        return "/friendshiping"
    elif "유수현" in text:
        return "/suhyeon"
    elif "보겸" in text:
        return "/bokyem"
    elif "럽미" in text:
        return "/loveme"
    elif "지식줄고양" in text:
        return "/cat"
        
def transform_datetime(publish_time):
    publish_time = datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%SZ")
    publish_time += timedelta(hours=9)
    return publish_time

def is_short_video(duration):
    """동영상이 Shorts인지 확인 (true/false로 반환)"""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return "true" if total_seconds <= 60 else "false"
    return "false"

