import re
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

