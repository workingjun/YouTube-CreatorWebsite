from DB.database import CommentDataManager, CombinedDataManager, VideoIdManager
from dataclasses import dataclass
import re
from datetime import datetime

@dataclass
class DBManager:
    Comments: CommentDataManager
    VideoId: VideoIdManager
    Combine: CombinedDataManager

def load_template():
    with open("template/template.html", "r", encoding="utf-8") as file:
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
    publish_time_list=list(publish_time.replace("T", " ").replace("Z", ""))
    previous_time = "".join(publish_time_list[11:13])
    plus_time = int(previous_time) + 9
    publish_time_list[11:13] = str(plus_time)
    publish_time = "".join(publish_time_list)  
    return datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")  

def is_short_video(duration):
    """동영상이 Shorts인지 확인"""
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if match:
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds <= 60
    return False
