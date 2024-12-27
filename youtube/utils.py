import re
from datetime import datetime
from DB.DataBase import CommentDataManager, CombinedDataManager, VideoIdManager, VideoDataManager


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