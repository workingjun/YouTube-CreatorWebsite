from datetime import datetime
from datetime import timedelta

def load_template():
    with open("templates/template.html", "r", encoding="utf-8") as file:
        template = file.read()
        template = template.replace("{", "{{").replace("}", "}}")
        template = template.replace("{{video_cards}}", "{video_cards}")
        template = template.replace("{{last_video_cards}}", "{last_video_cards}")
        template = template.replace("{{channel_info}}", "{channel_info}")
        return template

def load_main():
    with open("templates/template_main.html", "r", encoding="utf-8") as file:
        template = file.read()
        template = template.replace("{", "{{").replace("}", "}}")
        template = template.replace("{{container}}", "{container}")
        return template

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

def parse_duration_to_timedelta(duration):
    """
    ISO 8601 PT 형식을 timedelta로 변환
    """
    if not duration.startswith("PT"):
        raise ValueError(f"Invalid duration format: {duration}")

    # "PT" 제거 후 남은 부분을 분석
    duration = duration[2:]
    hours = 0
    minutes = 0
    seconds = 0
    num = ""

    for char in duration:
        if char.isdigit():
            num += char
        elif char == "H":
            hours = int(num)
            num = ""
        elif char == "M":
            minutes = int(num)
            num = ""
        elif char == "S":
            seconds = int(num)
            num = ""
        else:
            raise ValueError(f"Unexpected character in duration: {char}")

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def is_short_video(duration):
    """
    동영상이 Shorts인지 확인 (1 또는 0 반환)
    """
    try:
        td = parse_duration_to_timedelta(duration)
        return 1 if td.total_seconds() <= 60 else 0
    except ValueError as e:
        print(e)
        return 0  # 잘못된 형식은 Shorts가 아님
